#!/usr/bin/env
# uncomment below to stop script from running
#exit 0

#set -o nounset
set -o errexit
set -o pipefail
[[ "${DEBUG}" == 'true' ]] && set -o xtrace

cd src/fsharp
dotnet build

cd ../..
cd test/fsharp
dotnet build

cd ../..
cd src/csharp
dotnet build

cd ../..
cd test/csharp
dotnet build


cd ../..
cd deploy
rm ./* -f
cp ../src/fsharp/obj/Debug/netcoreapp2.1/*.* ./
cp ../src/csharp/obj/Debug/netcoreapp2.1/*.* ./
cp ../src/python37/*.* ./
zip airtable-sync-lambda.zip ./*

