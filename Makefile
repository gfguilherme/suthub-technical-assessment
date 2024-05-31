.PHONY: build-age-groups deploy-age-groups build-enrollment deploy-enrollment deploy-all

build-age-groups-api-stack:
	sam build --template age-groups-api/template.yml --build-dir age-groups-api/.aws-sam/build

deploy-age-groups-api-stack: build-age-groups-api-stack
	sam deploy --template age-groups-api/.aws-sam/build/template.yaml --stack-name age-groups-api-stack --capabilities CAPABILITY_IAM --resolve-s3

build-enrollment-api-stack:
	sam build --template enrollment-api/template.yml --build-dir enrollment-api/.aws-sam/build

deploy-enrollment-api-stack: build-enrollment-api-stack
	sam deploy --template enrollment-api/.aws-sam/build/template.yaml --stack-name enrollment-api-stack --capabilities CAPABILITY_IAM --resolve-s3

deploy-all: deploy-age-groups-api-stack deploy-enrollment-api-stack