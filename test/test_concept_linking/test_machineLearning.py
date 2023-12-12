import unittest
from unittest.mock import MagicMock, patch, mock_open
import torch
from torch.utils.data import DataLoader
from concept_linking.solutions.MachineLearning.src.model_training import train_model
from concept_linking.solutions.MachineLearning.src.model_module import ModelClass
from concept_linking.solutions.MachineLearning.src.training_dataset import TrainingDataset
from concept_linking.solutions.MachineLearning.src.config import TrainingConfig, ModelConfig
from concept_linking.solutions.MachineLearning.src.data_preprocessing import split_data, load_data, extract_sentences
import json
from sklearn.model_selection import train_test_split


class TestMachineLearning(unittest.TestCase):

    def setUp(self):
        self.data = [{"sentences": ["sentence " + str(i)]} for i in range(100)]

    def test_correct_split_ratio(self):
        train_data, val_data, test_data = split_data(self.data, test_size=0.2, val_size=0.5, random_state=42)

        # Check if the split ratios are correct
        self.assertEqual(len(train_data), 80)  # 80% for training
        self.assertEqual(len(val_data), 10)    # 10% for validation
        self.assertEqual(len(test_data), 10)   # 10% for testing

    def test_error_on_insufficient_samples(self):
        # Test with insufficient data
        small_data = [{"sentences": ["sentence 1", "sentence 2"]}]

        test_size = 0.5  # This will take 1 sentence for testing, leaving 1 for training and validation
        val_size = 0.5  # Doesn't matter in this case, as there's only 1 sentence left

        with self.assertRaises(ValueError):
            split_data(small_data, test_size=test_size, val_size=val_size, random_state=42)

    def test_reproducibility_with_random_state(self):
        train_data1, val_data1, test_data1 = split_data(self.data, test_size=0.2, val_size=0.5, random_state=42)
        train_data2, val_data2, test_data2 = split_data(self.data, test_size=0.2, val_size=0.5, random_state=42)

        # Check if the splits are the same with the same random state
        self.assertEqual(train_data1, train_data2)
        self.assertEqual(val_data1, val_data2)
        self.assertEqual(test_data1, test_data2)

    def test_load_data(self):
        mock_data = {'key': 'value'}
        mock_file_content = json.dumps(mock_data)
        with patch("builtins.open", mock_open(read_data=mock_file_content)) as mock_file:
            result = load_data("dummy_path.json")
            mock_file.assert_called_with("dummy_path.json", 'r', encoding='utf-8')
            self.assertEqual(result, mock_data)

    def test_extract_sentences(self):
        mock_data = [
            {"sentences": ["sentence 1", "sentence 2"]},
            {"sentences": ["sentence 3"]},
            {}  # Test with no 'sentences' key
        ]
        expected_sentences = ["sentence 1", "sentence 2", "sentence 3"]
        result = extract_sentences(mock_data)
        self.assertEqual(result, expected_sentences)

#class TestTrainModel(unittest.TestCase):
#
#    def setUp(self):
#        # Mock training and validation data
#        self.mock_train_data = [
#            {"sentence": "Example training sentence.", "entityMentions": [{"classification": "Person"}]},
#            {"sentence": "Another training sentence.", "entityMentions": [{"classification": "Organisation"}]}
#        ]
#        self.mock_val_data = [
#            {"sentence": "Example validation sentence.", "entityMentions": [{"classification": "Place"}]},
#            {"sentence": "Another validation sentence.", "entityMentions": [{"classification": "Person"}]}
#        ]
#
#        # Mock a model with parameters
#        self.mock_model = MagicMock(spec=ModelClass)
#        mock_param = torch.nn.Parameter(torch.randn(2, 2), requires_grad=True)
#        self.mock_model.parameters.return_value = [mock_param]
#
#        # Mock TrainingDataset and DataLoader
#        self.mock_training_dataset = MagicMock(spec=TrainingDataset)
#        self.mock_training_dataset.__len__.return_value = len(self.mock_train_data)
#        self.mock_training_dataset.__getitem__.side_effect = lambda idx: {'input': torch.tensor([0]),
#                                                                          'target': torch.tensor([1]), 'length': 1}
#
#        self.mock_val_dataset = MagicMock(spec=TrainingDataset)
#        self.mock_val_dataset.__len__.return_value = len(self.mock_val_data)
#        self.mock_val_dataset.__getitem__.side_effect = lambda idx: {'input': torch.tensor([0]),
#                                                                     'target': torch.tensor([1]), 'length': 1}
#
#        # Mock DataLoader to return an iterator over your mock data
#        self.mock_data_loader = MagicMock(spec=DataLoader)
#        self.mock_data_loader.return_value = iter(
#            [{'input': torch.tensor([0]), 'target': torch.tensor([1]).unsqueeze(0), 'length': 1}])
#
#        # Patching the actual classes with mocks
#        self.dataset_patcher = patch('concept_linking.solutions.MachineLearning.src.model_training.TrainingDataset',
#                                     side_effect=[self.mock_training_dataset, self.mock_val_dataset])
#        self.dataloader_patcher = patch('torch.utils.data.DataLoader', self.mock_data_loader)
#        self.model_class_patcher = patch('concept_linking.solutions.MachineLearning.src.model_training.ModelClass',
#                                         return_value=self.mock_model)
#        self.torch_load_patcher = patch('torch.load', return_value=self.mock_model.state_dict())
#        self.model_class_patcher.start()
#        self.torch_load_patcher.start()
#
#        self.dataset_patcher.start()
#        self.dataloader_patcher.start()
#        self.model_class_patcher.start()
#        self.torch_load_patcher.start()
#
#    def tearDown(self):
#        self.dataset_patcher.stop()
#        self.dataloader_patcher.stop()
#        self.model_class_patcher.stop()
#        self.torch_load_patcher.stop()
#
#
#
#    def test_train_model_with_no_initial_model(self):
#        # Test train_model when no initial model is provided
#        with patch('concept_linking.solutions.MachineLearning.src.model_training.ModelClass') as MockModelClass:
#            MockModelClass.return_value = MagicMock(spec=ModelClass)
#            result_model = train_model(self.mock_train_data, self.mock_val_data, model_name=None, model=None, config=TrainingConfig)
#
#            self.assertIsNotNone(result_model, "Model should be created when none is provided.")
#            MockModelClass.assert_called_with(TrainingConfig.input_size, TrainingConfig.embedding_dim, TrainingConfig.hidden_size, TrainingConfig.num_classes)
#
#    def test_train_model_with_initial_model(self):
#        # Test train_model when an initial model is provided
#        mock_existing_model = MagicMock(spec=ModelClass)
#        result_model = train_model(self.mock_train_data, self.mock_val_data, model_name=None, model=mock_existing_model, config=TrainingConfig)
#
#        self.assertIs(result_model, mock_existing_model, "The returned model should be the same as the provided initial model.")
#
#    def test_training_loop(self):
#        # Mocking a single batch for simplicity
#        mock_batch = {'input': [0], 'target': [1], 'length': [1]}
#        self.mock_data_loader.__iter__.return_value = [mock_batch]
#
#        # Mock the model's forward and backward methods
#        mock_model = MagicMock(spec=ModelClass)
#        train_model(self.mock_train_data, self.mock_val_data, model_name=None, model=mock_model, config=TrainingConfig)
#
#        mock_model.train.assert_called()
#        mock_model.zero_grad.assert_called()
#        mock_model.step.assert_called()
#
#
#    def test_validation_loop(self):
#        # Mocking a single batch for simplicity
#        mock_batch = {'input': [0], 'target': [1], 'length': [1]}
#        self.mock_data_loader.__iter__.return_value = [mock_batch]
#
#        mock_model = MagicMock(spec=ModelClass)
#        train_model(self.mock_train_data, self.mock_val_data, model_name=None, model=mock_model, config=TrainingConfig)
#
#        mock_model.eval.assert_called()
#
#    def test_model_saving(self):
#        # Test that the model state dictionary is saved
#        with patch('torch.save') as mock_save:
#            train_model(self.mock_train_data, self.mock_val_data, model_name='updated_model.pth', model=None, config=TrainingConfig)
#            mock_save.assert_called_once()  # Ensure it's called once
#            args, kwargs = mock_save.call_args
#            self.assertIn('updated_model.pth', args, "Model should be saved to 'updated_model.pth'.")




if __name__ == '__main__':
    unittest.main()