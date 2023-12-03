import os
import sys
import logging

from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from qcloud_cos import CosServiceError
from qcloud_cos import CosClientError
from qcloud_cos.cos_threadpool import SimpleThreadPool

import rich
from rich.logging import RichHandler
from rich.progress import track as richTrack

try:exit
except:from sys import exit

logging.basicConfig(level='NOTSET',
                    format='%(message)s',
                    datefmt='[%X]',
                    handlers=[RichHandler()])
log = logging.getLogger()

# or other path
with open('C:\\Users\\13750\\.orbstudio\\ls\\al_cos.sk') as fp:
    uploadInfo = eval(fp.read())

config = CosConfig(Region=uploadInfo['Region'],
                   SecretId=uploadInfo['SecretId'],
                   SecretKey=uploadInfo['SecretKey'],
                   Token=uploadInfo['Token'],
                   Scheme=uploadInfo['Scheme'])
client = CosS3Client(config)


upload_thread_pool = SimpleThreadPool()
for rpath, dirs, files in richTrack(os.walk(os.sep.join(__file__.split(os.sep)[:-1]))):
    for file in files:
        srckey = os.path.join(rpath,file)
        cosObjectKey = srckey.strip(os.sep)
        try:
            response = client.head_object(Bucket=uploadInfo['pool'], Key=cosObjectKey)
        except CosServiceError as e:
            log.error(f'Upload Failed: StatusCode {e.get_status_code()}: FilePath {file}')
        
        log.info(f'Add task: File {file}')
        upload_thread_pool.add_task(client.upload_file, uploadInfo['pool'], cosObjectKey, srckey)

upload_thread_pool.wait_completion()
if not upload_thread_pool.get_result()['success_all']:
    log.error('Not all files upload successed. Try again later')
else:
    log.info('Upload Successed')

