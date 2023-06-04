def host_arguments(parser):
    parser.add_argument('bucket_name', type=str, help="Pass bucket name.")

    parser.add_argument("-source",
                        "--source",
                        type=str,
                        help="host static configuration",
                        default=None)

    return parser


def vpc_arguments(parser):
    parser.add_argument('create', type=str, help="Pass bucket name.")

    parser.add_argument("-tag",
                        "--tag",
                        type=str,
                        help="tag vpc name",
                        default=None)

    parser.add_argument("-quantity",
                        "--quantity",
                        type=str,
                        help="quantity of public and private subnets",
                        default=None)

    return parser


def instance_arguments(parser):
    parser.add_argument('create', type=str, help="create instance.")

    parser.add_argument("-vpcid",
                        "--vpcid",
                        type=str,
                        help="give vpc id",
                        default=None)

    parser.add_argument("-subnetid",
                        "--subnetid",
                        type=str,
                        help="give subnet id",
                        default=None)

    return parser
