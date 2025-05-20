#CMN="--compilation_steps_only"
#CMN="--server staging"


echo
echo "1: "
certoraRun $CMN  certora/conf/.conf \
            --msg "1. .conf"
