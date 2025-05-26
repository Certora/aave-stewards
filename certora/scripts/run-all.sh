#CMN="--compilation_steps_only"
#CMN="--server staging"


echo
echo "1: rules.conf"
certoraRun $CMN  certora/conf/rules.conf \
            --msg "1. rules.conf"
