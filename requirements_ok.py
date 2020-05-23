import argparse
import sys
import pkg_resources
from pkg_resources import DistributionNotFound, VersionConflict

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('input', nargs='+', help="File name of path - only give 1")

    args = parser.parse_args()
    print(repr(args))
    assert len(args.input) == 1 

    try:
        files = {}
        for f_in_name in args.input:
            with open(f_in_name) as f_in:
                files[f_in_name] = [x.replace("\n",'').replace("\r",'') for x in f_in.readlines()]
    except IOError:
        print("Can NOT read FILE!")
        files[args.input[0]] = []
        open("/requirements.installed", 'a').close()
        
    return_exit_code = 0 

    dependencies = files[args.input[0]] 

    # here, if a dependency is not met, a DistributionNotFound or VersionConflict
    # exception is thrown. 
    try:
        pkg_resources.require(dependencies)
    except DistributionNotFound:
        print("DistributionNotFound")
        return_exit_code =1 
    except VersionConflict:
        print("VersionConflict")
        return_exit_code =1 
    except Exception as ex:
        print("{}".format(repr(ex)))
        return_exit_code = 2 

    print("Comparison - Exit code  {}".format(return_exit_code))

    if return_exit_code > 0 :
        import os
        os.remove("/requirements.installed")

    #sys.exit(return_exit_code)