export user_type="test"
export test_dir="tests"
export ignores="FOO"  # dummy file!

if [ -z $1 ]
then
    export capture=""
else
    export capture="--nocapture"
fi

export INDRA_HOME="./test_data"

echo "INDRA_HOME: $INDRA_HOME"
nosetests --ignore-files=$ignores --exe --verbose --with-coverage --cover-package=APIServer $capture

