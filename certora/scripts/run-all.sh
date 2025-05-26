#CMN="--compilation_steps_only"
#CMN="--server staging"


echo
echo "1: rules.conf"
certoraRun $CMN  certora/confs/rules.conf \
            --msg "1. rules.conf"
