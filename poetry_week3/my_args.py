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

    return parser
