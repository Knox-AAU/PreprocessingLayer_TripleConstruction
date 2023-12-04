from relation_extraction.NaiveMVP.main import handle_relation_post_request
from relation_extraction.multilingual.main import begin_relation_extraction


class RelationExtractor():
    @classmethod
    def begin_extraction(self, data):
        handle_relation_post_request(data)
        begin_relation_extraction(data)
