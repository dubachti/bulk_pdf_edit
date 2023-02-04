from argparse import ArgumentParser
import bulk_lib

def main():

    parser = ArgumentParser()

    parser.add_argument("-p", "--Path", dest="path",
                    help="path to dictionry", default="", type=str, required=True)

    parser.add_argument("-a", "--Action", dest="action",
                    help="select type of action to dictionary", default="", type=str, required=True, choices=bulk_lib.ALL_ACTIONS)

    parser.add_argument("-w", "--Overwrite", dest="overwrite",
                    help="overwrite file or create new instance", default=False, type=bool, required=False, )
    
    parser.add_argument("-o", "--Opacity", dest="opacity_val",
                    help="opacity val of output img in %", default=1, type=int, required=False, choices=range(0,101))

    args = parser.parse_args()

    bulk_lib.bulk_handler(vars(args))
    
    print(f"finished with action: {args.action}")


if __name__=='__main__':
    main()


