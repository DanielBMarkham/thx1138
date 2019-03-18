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
zip deploy/airtable-sync-lambda.zip src/fsharp/obj/Debug/netcoreapp2.1/*.* src/csharp/obj/Debug/netcoreapp2.1/*.* src/python37/*.*

