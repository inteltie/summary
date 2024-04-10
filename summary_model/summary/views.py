from rest_framework.views import APIView
from rest_framework.response import Response
from .tasks import generate_summary
import logging
from .custom_permission import ApiKeyPermission
logger = logging.getLogger('django')

class Summary(APIView):

    permission_classes = [ApiKeyPermission]

    def get(self,request,meeting_id):
        data = {
            'success':True,
        }
        try :
            generate_summary.delay(meeting_id)
            return Response(data)
        except Exception as err :
            data['success'] = False
            data['error'] = str(err)
            logger.warning(str(err))
            return Response(data)