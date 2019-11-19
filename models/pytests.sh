export user_type="test"
export test_dir="tests"
export ignores="scheduler, sandpile"

if [ -z $1 ]
then
    export capture=""
else
    export capture="--nocapture"
fi

# nose isn't finding tests at present, so we need to skip coverage:
nosetests --ignore-files=$ignores --exe --verbose $capture
# nosetests --ignore-files=$ignores --exe --verbose --with-coverage --cover-package=models $capture

