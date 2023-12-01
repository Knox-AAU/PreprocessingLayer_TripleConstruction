from relation_extraction.NaiveMVP.main import handle_relation_post_request


class RelationExtractor():
    @classmethod
    def begin_extraction(self, data):
        handle_relation_post_request(data)
