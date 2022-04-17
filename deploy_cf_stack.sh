#!/bin/bash
set +x

project="$1"
cf_template="$2"
stack_name="$3"
parameter_overrides="$4"
tags="$5"
deploy_s3_bucket="$6"
ecr_repo="$7"

echo 'Current directory:'
pwd

aws cloudformation package \
			--template-file ${cf_template}.yml \
			--s3-bucket ${deploy_s3_bucket} \
			--force-upload \
			--output-template-file ${cf_template}-compiled-template.yml
	export SAM_CLI_TELEMETRY=0 && \
	sam deploy --debug \
		--template-file ${cf_template}-compiled-template.yml \
		--capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
		--stack-name ${stack_name} \
		--region ${AWS_DEFAULT_REGION} \
		--image-repository ${ecr_repo} \
		--parameter-overrides ${parameter_overrides} \
		--no-fail-on-empty-changeset \
		--tags ${tags}

