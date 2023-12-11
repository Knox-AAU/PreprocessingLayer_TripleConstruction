import unittest
from unittest.mock import MagicMock, patch
from concept_linking.solutions.MachineLearning.src.model_training import train_model
from concept_linking.solutions.MachineLearning.src.training_dataset import TrainingDataset
import json

class TestTrainModel(unittest.TestCase):


    def setUp(self):
        # Creating mock JSON data for training and validation
        self.mock_train_data_json = json.dumps([
            {
                "language": "en",
                "metadataId": "example_id_train",
                "sentences": [
                    {
                        "sentence": "Explore the hidden corners of Dpdec nhotmqln iddogib to uncover its splendors",
                        "sentenceStartIndex": 0,
                        "sentenceEndIndex": 77,
                        "entityMentions": [
                            {
                                "name": "Dpdec nhotmqln iddogib",
                                "type": "Entity",
                                "label": "Place",
                                "startIndex": None,
                                "endIndex": None,
                                "iri": None,
                                "classification": "Place"
                            }
                        ]
                    }
                ]
            }
        ])
        self.mock_val_data_json = json.dumps([
            {
                "language": "en",
                "metadataId": "example_id_val",
                "sentences": [
                    {
                        "sentence": "Barrack Obama was married to Michelle Obama two days ago.",
                        "sentenceStartIndex": 20,
                        "sentenceEndIndex": 62,
                        "entityMentions": [
                            {
                                "name": "Barrack Obama",
                                "type": "Entity",
                                "label": "PERSON",
                                "startIndex": 0,
                                "endIndex": 12,
                                "iri": "knox-kb01.srv.aau.dk/Barack_Obama",
                                "classification": "Person"
                            }
                        ]
                    }
                ]
            }
        ])
        self.mock_config = train_model(self.mock_train_data_json,self.mock_train_data_json).TrainingConfig() # Set mock config parameters

        # Patching the actual classes with mocks
        self.patcher1 = patch('train_model().TrainingDataset')
        self.patcher2 = patch('train_model().DataLoader')
        self.patcher3 = patch('train_model().ModelClass')
        self.mock_training_dataset = self.patcher1.start()
        self.mock_data_loader = self.patcher2.start()
        self.mock_model_class = self.patcher3.start()


        self.patcher4 = patch('builtins.open', new_callable=unittest.mock.mock_open, read_data=self.mock_train_data_json)
        self.patcher4.start()

    def tearDown(self):
        # Stop all patchers
        self.patcher1.stop()
        self.patcher2.stop()
        self.patcher3.stop()
        self.patcher4.stop()

    def test_train_model_with_no_initial_model(self):
        # Test train_model when no initial model is provided
        result_model = train_model(self.mock_train_data, self.mock_val_data, model=None, config=self.mock_config)

        self.assertIsNotNone(result_model, "Model should be created when none is provided.")
        self.assertIsInstance(result_model, train_model(self.mock_train_data_json,self.mock_val_data_jsons).ModelClass,
                              "The created model should be an instance of ModelClass.")

    def test_train_model_with_initial_model(self):
        # Test train_model when an initial model is provided
        mock_existing_model = MagicMock()
        result_model = train_model(self.mock_train_data, self.mock_val_data, model=mock_existing_model,
                                   config=self.mock_config)

        self.assertEqual(result_model, mock_existing_model,
                         "The returned model should be the same as the provided initial model.")

    def test_training_loop(self):
        # Mocking a single batch for simplicity
        mock_batch = {'input': [0], 'target': [1], 'length': [1]}
        self.mock_data_loader.__iter__.return_value = [mock_batch]

        # Mock the model's forward and backward methods
        mock_model = MagicMock()
        train_model(self.mock_train_data, self.mock_val_data, model=mock_model, config=self.mock_config)

        mock_model.train.assert_called()
        mock_model.zero_grad.assert_called()
        mock_model.step.assert_called()

    def test_validation_loop(self):
        # Mocking a single batch for simplicity
        mock_batch = {'input': [0], 'target': [1], 'length': [1]}
        self.mock_data_loader.__iter__.return_value = [mock_batch]

        mock_model = MagicMock()
        train_model(self.mock_train_data, self.mock_val_data, model=mock_model, config=self.mock_config)

        mock_model.eval.assert_called()

    def test_model_saving(self):
        # Test that the model state dictionary is saved
        with patch('torch.save') as mock_save:
            train_model(self.mock_train_data, self.mock_val_data, model=None, config=self.mock_config)
            mock_save.assert_called_once()  # Ensure it's called once
            args, kwargs = mock_save.call_args
            self.assertIn('updated_model.pth', args, "Model should be saved to 'updated_model.pth'.")


if __name__ == '__main__':
    unittest.main()