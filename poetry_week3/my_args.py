def host_arguments(parser):
    parser.add_argument('bucket_name', type=str, help="Pass bucket name.")

    parser.add_argument("-source",
                        "--source",
                        type=str,
                        help="host static configuration",
                        default=None)

    return parser
