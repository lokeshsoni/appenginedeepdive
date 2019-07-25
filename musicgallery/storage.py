import datetime

import cloudstorage
from flask import current_app
import six
from werkzeug import secure_filename
from werkzeug.exceptions import BadRequest


def _check_extension(filename, allowed_extensions):
    if ('.' not in filename or filename.split('.').pop().lower() not in allowed_extensions):
        raise BadRequest("{0} has an invalid name or extension".format(filename))


def _safe_filename(filename):
    filename = secure_filename(filename)
    date = datetime.datetime.utcnow().strftime("%Y-%m-%d-%H%M%S")
    basename, extension = filename.rsplit('.', 1)
    return "{0}-{1}.{2}".format(basename, date, extension)


def upload_file(file_stream, filename, content_type):
    _check_extension(filename, current_app.config['ALLOWED_EXTENSIONS'])
    filename = _safe_filename(filename)
    bucket = current_app.config['CLOUD_STORAGE_BUCKET']
    
    objectname = '/' + bucket + '/' + filename
    
    cs_file = cloudstorage.open(objectname, 'w', content_type=content_type)
    cs_file.write(file_stream)
    cs_file.close()

    url = 'https://storage.googleapis.com' + objectname

    if isinstance(url, six.binary_type):
       url = url.decode('utf-8')

    return url
