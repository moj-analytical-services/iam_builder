iam_base_template = {
    "Version": "2012-10-17",
    "Statement": []
}

athena_dump_bucket = "alpha-athena-query-dump"

iam_lookup = {
    "athena_read_access": [
        {
            "Sid": "AllowListAllMyBuckets",
            "Effect": "Allow",
            "Action": [
                "s3:GetBucketLocation",
                "s3:ListAllMyBuckets"
            ],
            "Resource": [
                "*"
            ]
        },
        {
            "Sid": "AllowListBucket",
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::moj-analytics-lookup-tables",
                "arn:aws:s3:::" + athena_dump_bucket
            ]
        },
        {
            "Sid": "AllowGetObject",
            "Effect": "Allow",
            "Action": [
                "s3:GetObject"
            ],
            "Resource": [
                "arn:aws:s3:::moj-analytics-lookup-tables/*"
            ]
        },
        {
            "Sid": "AllowGetPutObject",
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject"
            ],
            "Resource": [
                "arn:aws:s3:::aws-athena-query-results-*"
            ]
        },
        {
            "Sid": "AllowGetPutDeleteObject",
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:DeleteObject"
            ],
            "Resource": [
                "arn:aws:s3:::" + athena_dump_bucket + "/${aws:userid}/*"
            ]
        },
        {
            "Sid": "AllowReadAthenaGlue",
            "Effect": "Allow",
            "Action": [
                "athena:BatchGetNamedQuery",
                "athena:BatchGetQueryExecution",
                "athena:GetNamedQuery",
                "athena:GetQueryExecution",
                "athena:GetQueryResults",
                "athena:GetQueryResultsStream",
                "athena:GetWorkGroup",
                "athena:ListNamedQueries",
                "athena:ListWorkGroups",
                "athena:StartQueryExecution",
                "athena:StopQueryExecution",
                "athena:CancelQueryExecution",
                "athena:GetCatalogs",
                "athena:GetExecutionEngine",
                "athena:GetExecutionEngines",
                "athena:GetNamespace",
                "athena:GetNamespaces",
                "athena:GetTable",
                "athena:GetTables",
                "athena:RunQuery",
                "glue:GetDatabase",
                "glue:GetDatabases",
                "glue:GetTable",
                "glue:GetTables",
                "glue:GetPartition",
                "glue:GetPartitions",
                "glue:BatchGetPartition",
                "glue:GetCatalogImportStatus",
                "glue:GetUserDefinedFunction",
                "glue:GetUserDefinedFunctions"
            ],
            "Resource": [
                "*"
            ]
        }
    ],
    "athena_write_access": [
        {
            "Sid": "AllowWriteAthenaGlue",
            "Effect": "Allow",
            "Action": [
                "athena:DeleteNamedQuery",
                "glue:BatchCreatePartition",
                "glue:BatchDeletePartition",
                "glue:BatchDeleteTable",
                "glue:CreateDatabase",
                "glue:CreatePartition",
                "glue:CreateTable",
                "glue:DeleteDatabase",
                "glue:DeletePartition",
                "glue:DeleteTable",
                "glue:UpdateDatabase",
                "glue:UpdatePartition",
                "glue:UpdateTable",
                "glue:CreateUserDefinedFunction",
                "glue:DeleteUserDefinedFunction",
                "glue:UpdateUserDefinedFunction"
            ],
            "Resource": [
                "*"
            ]
        }
    ],
    "glue_job": [
        {
            "Sid": "GlueJobActions",
            "Effect": "Allow",
            "Action": [
                "glue:BatchStopJobRun",
                "glue:CreateJob",
                "glue:DeleteJob",
                "glue:GetJob",
                "glue:GetJobs",
                "glue:GetJobRun",
                "glue:GetJobRuns",
                "glue:StartJobRun",
                "glue:UpdateJob",
                "glue:ListJobs",
                "glue:BatchGetJobs",
                "glue:GetJobBookmark"
            ],
            "Resource": [
                "*"
            ]
        },
        {
            "Sid": "CanGetLogs",
            "Effect": "Allow",
            "Action": [
                "logs:GetLogEvents",
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents",
                "logs:DescribeLogStreams"
            ],
            "Resource": [
                "arn:aws:logs:*:*:/aws-glue/*"
            ]
        },
        {
            "Sid": "CanGetCloudWatchLogs",
            "Effect": "Allow",
            "Action": [
                "cloudwatch:PutMetricData",
                "cloudwatch:GetMetricData",
                "cloudwatch:ListDashboards"
            ],
            "Resource": [
                "*"    
            ]
        },
        {
            "Sid": "CanReadGlueStuff",
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject"
            ],
            "Resource": [
                "arn:aws:s3:::aws-glue-*/*",
                "arn:aws:s3:::*/*aws-glue-*/*",
                "arn:aws:s3:::aws-glue-*"
            ]
        }
    ],
    "decrypt_statement": [
        {
            "Sid": "allowDecrypt",
            "Effect": "Allow",
            "Action": [
                "kms:Decrypt"
            ],
            "Resource": [
                "arn:aws:kms:::key/*"
            ]
        }
    ]
}

def get_pass_role_to_glue_policy(iam_role):
    policy = {
                "Sid": "PassRoleToGlueService",
                "Effect": "Allow",
                "Action": [
                    "iam:PassRole"
                ],
                "Resource": "arn:aws:iam::593291632749:role/{}".format(iam_role),
                "Condition": {
                    "StringLike": {
                        "iam:PassedToService": [
                            "glue.amazonaws.com"
                        ]
                    }
                }
            }
    return policy

def get_read_only_policy(list_of_s3_paths):
    list_of_s3_paths = add_s3_arn_prefix(list_of_s3_paths)
    policy = {
            "Sid": "readonly",
            "Action": [
                "s3:GetObject",
                "s3:GetObjectAcl",
                "s3:GetObjectVersion",
            ],
            "Effect": "Allow",
            "Resource": list_of_s3_paths,
        }
    return policy

def get_write_only_policy(list_of_s3_paths):
    list_of_s3_paths = add_s3_arn_prefix(list_of_s3_paths)
    policy = {
            "Sid": "writeonly",
            "Action": [
                "s3:DeleteObject",
                "s3:DeleteObjectVersion",
                "s3:PutObject",
                "s3:PutObjectAcl",
                "s3:RestoreObject"
            ],
            "Effect": "Allow",
            "Resource": list_of_s3_paths,
        }
    return policy

def get_read_write_policy(list_of_s3_paths):
    list_of_s3_paths = add_s3_arn_prefix(list_of_s3_paths)
    policy = {
        "Sid": "readwrite",
        "Action": [
            "s3:GetObject",
            "s3:GetObjectAcl",
            "s3:GetObjectVersion",
            "s3:DeleteObject",
            "s3:DeleteObjectVersion",
            "s3:PutObject",
            "s3:PutObjectAcl",
            "s3:RestoreObject",
        ],
        "Effect": "Allow",
        "Resource": list_of_s3_paths,
    }
    return policy

def get_s3_list_bucket_policy(list_of_buckets):
    list_of_buckets = add_s3_arn_prefix(list_of_buckets)
    policy = {
        "Sid": "list",
        "Action": [
            "s3:ListBucket",
            "s3:ListAllMyBuckets",
            "s3:GetBucketLocation"
        ],
        "Effect": "Allow",
        "Resource": sorted(list(set(list_of_buckets))),
    }
    return policy

def add_s3_arn_prefix(paths):
    arn_prefix = 'arn:aws:s3:::'
    return [arn_prefix + p for p in paths]

def get_secrets(iam_role):
    statement = {
        "Sid": "readParams",
        "Effect": "Allow",
        "Action": [
            "ssm:DescribeParameters",
            "ssm:GetParameter",
            "ssm:GetParameters",
            "ssm:GetParameterHistory",
            "ssm:GetParametersByPath"
        ],
        "Resource": [
            f"arn:aws:ssm:*:*:parameter/alpha/airflow/{iam_role}/*"
        ]
    }
    return statement
