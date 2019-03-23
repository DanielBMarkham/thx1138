namespace AWSLambda1


open Amazon.Util
open Amazon.Lambda.Core

open Amazon.S3
open Amazon.S3.Util
open System



// Assembly attribute to enable the Lambda function's JSON input to be converted into a .NET class.
[<assembly: LambdaSerializer(typeof<Amazon.Lambda.Serialization.Json.JsonSerializer>)>]
()


type FSFunction(s3Client: IAmazonS3) =
    new() = FSFunction(new AmazonS3Client())

    /// <summary>
    /// This method is called for every Lambda invocation. This method takes in an S3 event object and can be used
    /// to respond to S3 notifications.
    /// </summary>
    /// <param name="event"></param>
    /// <param name="context"></param>
    /// <returns></returns>
    member __.lambda_handler (event:string) (context: ILambdaContext) =
        // PYTHON S3 CODE
        // s3 = boto3.resource('s3')
        // print('put %s/%s' % (BUCKET, FILENAME))
        // hours = int(os.environ.get('CACHE_HOURS', 6))
        // expires_dt = (datetime.now() + timedelta(hours=hours))
        // s3.Object(BUCKET, FILENAME).put(
        //     Body=json.dumps(data),
        //     ContentType='application/json',
        //     ACL=os.environ.get('ACL', 'public-read'),
        //     Expires=expires_dt
        // )
        // Now do this in f# (no error handling, of course! ha!)

        let processEvent (event:string) (context: ILambdaContext) = async {
            let bucket=context.ClientContext.Environment.Item("S3_BUCKET")
            let filename="foobar.txt"
            printf "put %s/%s"  bucket filename
            let hours=context.ClientContext.Environment.Item("CACHE_HOURS")
            let expiresDate=System.DateTime.Now.AddHours(Double.Parse(hours))
            let req=Model.PutObjectRequest(
                        BucketName=bucket,
                        Key=filename,
                        ContentBody="I exist"
                        )
            let! resp=s3Client.PutObjectAsync(req) |> Async.AwaitTask
            return resp
            }
        processEvent event context
        |> Async.RunSynchronously


        // let fetchContentType (s3Event: S3EventNotification.S3Entity) = async {
        //     sprintf "Processing object %s from bucket %s" s3Event.Object.Key s3Event.Bucket.Name
        //     |> context.Logger.LogLine

        //     let! response =
        //         s3Client.GetObjectMetadataAsync(s3Event.Bucket.Name, s3Event.Object.Key)
        //         |> Async.AwaitTask

        //     sprintf "Content Type %s" response.Headers.ContentType
        //     |> context.Logger.LogLine

        //     return response.Headers.ContentType
        // }
 
        // fetchContentType (event.Records.Item(0).S3)
        // |> Async.RunSynchronously