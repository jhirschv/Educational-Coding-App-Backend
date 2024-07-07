from django.shortcuts import render
import docker
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CodeSerializer
import tempfile
import os

def escape_double_quotes(code):
    # Escape double quotes in the code string
    return code.replace('"', '\\"')

class ExecuteCode(APIView):
    def post(self, request):
        serializer = CodeSerializer(data=request.data)
        if serializer.is_valid():
            code = serializer.validated_data['code']
            escaped_code = escape_double_quotes(code)
            client = docker.from_env()
            
            # Create a temporary file to save the code
            with tempfile.NamedTemporaryFile(delete=False, suffix='.py') as temp_file:
                temp_file.write(code.encode('utf-8'))
                temp_file_path = temp_file.name

            try:
                
                # Running the Docker container with the user's code
                container = client.containers.run(
                    'my-python-app',
                    command=f'/app/{os.path.basename(temp_file_path)}',
                    volumes={os.path.dirname(temp_file_path): {'bind': '/app', 'mode': 'rw'}},
                    working_dir='/app',
                    detach=True,
                    stdout=True,
                    stderr=True,
                    network_disabled=True,
                )

                # Wait for the container to finish and capture the output
                container.wait()
                output = container.logs()

                # Remove the temporary file after execution
                os.remove(temp_file_path)

                return Response({'result': output.decode('utf-8')}, status=status.HTTP_200_OK)
            except docker.errors.ContainerError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
