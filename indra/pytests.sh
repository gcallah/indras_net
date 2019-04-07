export user_type="test"
export test_dir="tests"
export ignores="FOO"
if [ "$USER" == "arnavshah" ]
then
    export ignores="test_user\.py"
fi

nosetests --ignore-files=$ignores --exe --verbose --with-coverage --cover-package=indra

#--ignore-files="$ignores"
