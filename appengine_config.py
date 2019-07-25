from google.appengine.ext import vendor
import tempfile
import tempfile2
tempfile.SpooledTemporaryFile = tempfile2.SpooledTemporaryFile

vendor.add('lib')
