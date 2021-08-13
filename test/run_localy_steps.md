1. Run docker container - `docker run -ti --rm -v ${PWD}:/ardens-processing -v c:/Users/andbud/.aws:/root/.aws -v c:/Users/andbud/.ssh:/root/.ssh boto3_image:latest bash`

1. Upgrade packages - `apt upgrade`

1. Install mc commander - `apt instal mc`

1. Upgrade pip and install modules - `python -m pip install --upgrade pip` and `pip install pymysql`

1. Make SSH tunnel in the same container, but from other terminal - `ssh -N -L 3306:qa-ardensmanager.cvkraaeo3n1z.eu-west-2.rds.amazonaws.com:3306 andbud@18.135.125.22`

1. Run script - `python uidb_connect.py`