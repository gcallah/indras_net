export user_type="test"
export test_dir="tests"
export ignores="FOO"
echo "$INDRA_HOME"
if [ "$USER" == "arnavshah" ]; then
  export ignores="test_user\.py"
fi

if [ -z "$1" ]; then
  export capture=""
else
  export capture="--nocapture"
fi

nosetests --ignore-files=$ignores --exe --verbose --with-coverage --cover-package=indra $capture
