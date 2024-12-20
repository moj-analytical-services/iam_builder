# Formatted to match JSON IAM policy - so purposefully
# not matching standard Python line break conventions

iam_base_template = {
    "Version": "2012-10-17",
    "Statement": []
}


# Standard segments of iam policy that don't need parameters
iam_lookup = {
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
    "cadet_deployer": [
        {
            "Sid": "GlueCatalogActions",
            "Effect": "Allow",
            "Action": [
                "glue:Get*",
                "glue:DeleteTable",
                "glue:DeleteTableVersion",
                "glue:DeleteSchema",
                "glue:DeletePartition",
                "glue:DeleteDatabase",
                "glue:UpdateTable",
                "glue:UpdateSchema",
                "glue:UpdatePartition",
                "glue:UpdateDatabase",
                "glue:CreateTable",
                "glue:CreateSchema",
                "glue:CreatePartition",
                "glue:CreatePartitionIndex",
                "glue:BatchCreatePartition",
                "glue:CreateDatabase"
            ],
            "Resource": [
                "arn:aws:glue:*:*:schema/*",
                "arn:aws:glue:*:*:database/*",
                "arn:aws:glue:*:*:table/*/*",
                "arn:aws:glue:*:*:catalog"
            ]
        },
        {
            "Sid": "AthenaActions",
            "Effect": "Allow",
            "Action": [
                "athena:List*",
                "athena:Get*",
                "athena:StartQueryExecution",
                "athena:StopQueryExecution"
            ],
            "Resource": [
                "arn:aws:athena:*:*:datacatalog/*",
                "arn:aws:athena:*:*:workgroup/*"
            ]
        },
        {
            "Sid": "AirflowCLIPolicy",
            "Effect": "Allow",
            "Action": [
                "airflow:CreateCliToken"
            ],
            "Resource": [
                "arn:aws:airflow:*:*:environment/dev",
                "arn:aws:airflow:*:*:environment/prod"
            ]
        },
        {
            "Sid": "CadetWriteAccess",
            "Effect": "Allow",
            "Action": [
                "s3:List*",
                "s3:GetObject*",
                "s3:GetBucket*",
                "s3:DeleteObject*",
                "s3:PutObject*"
            ],
            "Resource": [
                "arn:aws:s3:::mojap-derived-tables/*",
                "arn:aws:s3:::mojap-derived-tables",
                "arn:aws:s3:::dbt-query-dump/*",
                "arn:aws:s3:::dbt-query-dump",
                "arn:aws:s3:::mojap-manage-offences/ho-offence-codes/*",
                "arn:aws:s3:::mojap-manage-offences",
                "arn:aws:s3:::mojap-hub-exports/probation_referrals_dump/*",
                "arn:aws:s3:::mojap-hub-exports",
                "arn:aws:s3:::alpha-app-opg-lpa-dashboard",
                "arn:aws:s3:::alpha-app-opg-lpa-dashboard/dev/models/domain_name=opg/*",
                "arn:aws:s3:::alpha-app-opg-lpa-dashboard/prod/models/domain_name=opg/*",
                "arn:aws:s3:::alpha-bold-data-shares",
                "arn:aws:s3:::alpha-bold-data-shares/reducing-reoffending/*"
            ]
        },
        {
            "Sid": "CadetReadAccess",
            "Effect": "Allow",
            "Action": [
                "s3:List*",
                "s3:GetObject*",
                "s3:GetBucket*"
            ],
            "Resource": [
                "arn:aws:s3:::*",
                "arn:aws:s3:::*/*"
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
    ],
    "bedrock": [
        {
            "Sid": "BedrockActions",
            "Effect": "Allow",
            "Action": [
                "bedrock:ListFoundationModels",
                "bedrock:GetFoundationModel",
                "bedrock:InvokeModel",
                "bedrock:InvokeModelWithResponseStream",
                "bedrock:CreateModelCustomizationJob",
                "bedrock:GetModelCustomizationJob",
                "bedrock:GetFoundationModelAvailability",
                "bedrock:ListModelCustomizationJobs",
                "bedrock:StopModelCustomizationJob",
                "bedrock:GetCustomModel",
                "bedrock:ListCustomModels",
                "bedrock:DeleteCustomModel",
                "bedrock:ListProvisionedModelThroughputs",
                "bedrock:ListTagsForResource",
                "bedrock:UntagResource",
                "bedrock:TagResource",
                "bedrock:CreateAgent",
                "bedrock:UpdateAgent",
                "bedrock:GetAgent",
                "bedrock:ListAgents",
                "bedrock:CreateActionGroup",
                "bedrock:UpdateActionGroup",
                "bedrock:GetActionGroup",
                "bedrock:ListActionGroups",
                "bedrock:CreateAgentDraftSnapshot",
                "bedrock:GetAgentVersion",
                "bedrock:ListAgentVersions",
                "bedrock:CreateAgentAlias",
                "bedrock:UpdateAgentAlias",
                "bedrock:GetAgentAlias",
                "bedrock:ListAgentAliases",
                "bedrock:InvokeAgent",
                "bedrock:PutFoundationModelEntitlement",
                "bedrock:GetModelInvocationLoggingConfiguration",
                "bedrock:PutModelInvocationLoggingConfiguration",
                "bedrock:CreateFoundationModelAgreement",
                "bedrock:DeleteFoundationModelAgreement",
                "bedrock:ListFoundationModelAgreementOffers",
                "bedrock:GetUseCaseForModelAccess"
            ],
            "Resource": ["*"],
            "Condition": {
                "StringEquals": {
                    "aws:RequestedRegion": [
                        "eu-central-1",
                        "eu-west-3",
                        "eu-west-2"
                    ]
                }
            }
        }
    ],
    "cloudwatch_athena_query_executions": [
        {
            "Sid": "CanGetCloudWatchAthenaLogs",
            "Effect": "Allow",
            "Action": [
                "logs:GetLogEvents",
                "logs:GetLogRecord"
            ],
            "Resource": [
                "arn:aws:logs:eu-west-2:593291632749:log-group:cloudtrail-athena-events:*"
            ]
        }
    ]
}


def get_athena_read_access(dump_bucket: list) -> dict:
    """Creates segments of IAM policy needed for reading
    from one or more Athena query dump buckets

    Parameters
    ----------
    dump_bucket (list): bucket name or names for Athena query dump
    """
    # prepare segments that depend on dump bucket name
    allow_list_bucket_resources = ["arn:aws:s3:::moj-analytics-lookup-tables"]
    allow_list_bucket_resources.extend([
        "arn:aws:s3:::" + bucket for bucket in dump_bucket
        ])
    allow_get_put_delete_resources = [
        "arn:aws:s3:::" + bucket + "/${aws:userid}/*" for bucket in dump_bucket
    ]

    # insert prepared sections into full iam lookup for Athena reading
    athena_read_access = [
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
                "Resource": allow_list_bucket_resources
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
                "Resource": allow_get_put_delete_resources
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
                    "athena:ListQueryExecutions",
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
                    "athena:GetTableMetadata",
                    "athena:RunQuery",
                    "glue:GetDatabase",
                    "glue:GetDatabases",
                    "glue:GetTable",
                    "glue:GetTableVersions",
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
        ]
    return athena_read_access


def get_pass_role_to_glue_policy(iam_role: str) -> dict:
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


def get_read_only_policy(list_of_s3_paths: list) -> dict:
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


def get_write_only_policy(list_of_s3_paths: list) -> dict:
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


def get_read_write_policy(list_of_s3_paths: list) -> dict:
    list_of_s3_paths = add_s3_arn_prefix(list_of_s3_paths)
    policy = {
        "Sid": "readwrite",
        "Action": [
            "s3:GetObject",
            "s3:GetObjectAcl",
            "s3:GetObjectVersion",
            "s3:GetObjectTagging",
            "s3:DeleteObject",
            "s3:DeleteObjectVersion",
            "s3:PutObject",
            "s3:PutObjectAcl",
            "s3:PutObjectTagging",
            "s3:RestoreObject",
        ],
        "Effect": "Allow",
        "Resource": list_of_s3_paths,
    }
    return policy


def get_deny_policy(list_of_s3_paths: list) -> dict:
    list_of_s3_paths = add_s3_arn_prefix(list_of_s3_paths)
    policy = {
        "Sid": "deny",
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
        "Effect": "Deny",
        "Resource": list_of_s3_paths,
    }
    return policy


def get_s3_list_bucket_policy(list_of_buckets: list) -> dict:
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


def add_s3_arn_prefix(paths: list) -> list:
    arn_prefix = "arn:aws:s3:::"
    return [arn_prefix + p for p in paths]


def get_secrets(iam_role: str, write=False) -> dict:
    if write:
        statement = {
            "Sid": "readwriteParams",
            "Effect": "Allow",
            "Action": [
                "ssm:DescribeParameters",
                "ssm:GetParameter",
                "ssm:GetParameters",
                "ssm:GetParameterHistory",
                "ssm:GetParametersByPath",
                "ssm:PutParameter",
                "ssm:DeleteParameter",
                "ssm:DeleteParameters"
            ],
            "Resource": [
                f"arn:aws:ssm:*:*:parameter/alpha/airflow/{iam_role}/*"
            ]
        }
    else:
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

def get_kms_permissions(kms_arns: list) -> dict:
    policy = {
        "Sid": "kmsPermissions",
        "Action": [
            "kms:ReEncrypt*",
            "kms:GenerateDataKey*",
            "kms:Encrypt",
            "kms:DescribeKey",
            "kms:Decrypt"
        ],
        "Effect": "Allow",
        "Resource": kms_arns,
    }
    return policy

def get_secretsmanager_read_only_policy(secrets: list) -> dict:
    # prepare segments that depend on dump bucket name
    allow_list_of_secrets = []
    allow_list_of_secrets.extend([
        "arn:aws:secretsmanager:*:*:secret:" + secret + "*" for secret in secrets
        ])
    policy = {
        "Sid": "readSecrets",
        "Action": [
            "secretsmanager:GetSecretValue",
            "secretsmanager:DescribeSecret",
            "secretsmanager:ListSecrets",
        ],
        "Effect": "Allow",
        "Resource": allow_list_of_secrets
    }
    return policy
