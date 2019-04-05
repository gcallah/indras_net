export user_type="test"
export test_dir="tests"
export ignores=""
if [ "$USER" == "gcallah" ]
then
    export ignores="$test_dir/test_user.py"
fi
echo "$ignores"
nosetests --exe --verbose --with-coverage --cover-package=indra2 -I $ignores

#--ignore-files="$ignores"
