export user_type="test"
export test_dir="tests"

if [ -z $1 ]
then
    export capture=""
else
    export capture="--nocapture"
fi

nosetests --exe --verbose --with-coverage --cover-package=ml $capture

