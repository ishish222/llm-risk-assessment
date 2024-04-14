all: dependencies_layer sample_lambda

dependencies_layer:
	mkdir -p ./build/artifacts/layer/python/lib/python3.10/site-packages/
	pip install -r requirements.txt --platform manylinux2014_x86_64 --only-binary=:all: -t ./build/artifacts/layer/python/lib/python3.10/site-packages/
	cd ./build/artifacts/layer && zip -r ../dependencies_layer.zip .

sample_lambda: 
	rm -rf ./build/artifacts/package
	mkdir -p ./build/artifacts/package
	cp ./src/lambda/sample_lambda.py ./build/artifacts/package
	cd ./build/artifacts/package && zip -r ../sample_lambda.zip .

clean:
	rm -rf ./build/*
	touch ./build/.gitkeep
