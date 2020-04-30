class Endpoint(object):
    @staticmethod
    def create_docs_session_path():
        return "/sessions"

    @staticmethod
    def retrieve_docs_session_path(session_id):
        return "/sessions/{sessionId}".format(sessionId=session_id)

    @staticmethod
    def delete_docs_session_path(session_id):
        return Endpoint.retrieve_docs_session_path(session_id)

    @staticmethod
    def get_media_content_path(session_id, media_id):
        return "/sessions/{sessionId}/media/{mediaId}/content".format(
            sessionId=session_id, mediaId=media_id
        )

    @staticmethod
    def delete_media_path(session_id, media_id):
        return Endpoint.get_media_content_path(session_id, media_id)

    @staticmethod
    def get_supported_documents_path():
        return "/supported-documents"
