from rest_framework.views import APIView
from rest_framework.response import Response

import ktrain, os

class FakeNewsCheckerView(APIView):
    
    def get(self, request, *args, **kwargs):
        news = request.query_params.get('news')
        title = request.query_params.get('title')
        author = request.query_params.get('author')
        total = str(title)+str(author)+str(news)
        path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ml", "predictor")
        model = ktrain.load_predictor(path)
        return Response({"isTrue": model.predict(total)})
    