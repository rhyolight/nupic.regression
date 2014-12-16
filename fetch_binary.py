import sys
import os
import requests
from boto.s3.connection import S3Connection
import shutil

REGION = "us-west-2"
BUCKET = "artifacts.numenta.org"
REPO = "numenta/nupic"
SHA_FILE = "nupic_sha.txt"
WHEEL_DIR = "wheel"
AWS_KEY = os.environ["AWS_ACCESS_KEY_ID"]
AWS_SECRET = os.environ["AWS_SECRET_ACCESS_KEY"]



def getScriptPath():
  return os.path.dirname(os.path.realpath(sys.argv[0]))



def fetchWheel(url, localFilePath):
  blockCount = 0
  with open(localFilePath, "wb") as handle:
    response = requests.get(url, stream=True)
    if not response.ok:
      raise Exception("Cannot fetch wheel from %s" % url)
    for block in response.iter_content(1024):
      if blockCount % 100 == 0:
        sys.stdout.write('.')
        sys.stdout.flush()
      blockCount += 1
      if not block:
        break
      handle.write(block)
    print "\nDone."



def fetchWheels(sha):
  conn = S3Connection(AWS_KEY, AWS_SECRET)
  artifactsBucket = conn.get_bucket(BUCKET)
  wheelDir = os.path.join(getScriptPath(), WHEEL_DIR)
  url = None

  # Here's where we put the wheels!
  if not os.path.exists(wheelDir):
    os.makedirs(wheelDir)

  for key in artifactsBucket.list(prefix="%s/%s" % (REPO, sha)):
    # Fail fast.
    if not key.name.endswith(".whl"):
      raise ValueError("Expected .whl file, found %s" % key.name)

    # Expects a key like:
    # numenta/nupic/9e17ca7caef03a2b1aa925e010ee76c1a74ec3cc/setuptools-8.0.4-py2.py3-none-any.whl
    print key.name
    wheelName = key.name.split("/").pop()

    url = "https://s3-%s.amazonaws.com/%s/%s" % (REGION, BUCKET, key.name)
    # Looks like:
    # https://s3-us-west-2.amazonaws.com/artifacts.numenta.org/numenta/nupic/9e17ca7caef03a2b1aa925e010ee76c1a74ec3cc/setuptools-8.0.4-py2.py3-none-any.whl

    localFilePath = os.path.join(wheelDir, wheelName)

    print "Fetching archive from %s..." % url
    fetchWheel(url, localFilePath)



def getSha():
  with open(SHA_FILE, "r") as shaFile:
    return shaFile.read().strip()



if __name__ == "__main__":
  sha = getSha()
  fetchWheels(sha)
