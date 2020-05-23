import argparse
import sys
import pkg_resources
from pkg_resources import DistributionNotFound, VersionConflict


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('input', nargs='+', help="File name of path - only give 2")

    args = parser.parse_args()
    assert len(args.input) == 2 
    
    print(repr(args))

    files = dict()

    for f_in_name in args.input:
        with open(f_in_name) as f_in:
            files[f_in_name] = [x.replace("\n",'').replace("\r",'') for x in f_in.readlines()]
    
    has_version = lambda ac_line : [ x for x in [ '~', '>', '<', '=' ] if x in ac_line ]
    
    return_exit_code = 0 
    
    found_pkgs = 0
    for a_line in files[args.input[0]]:
        if len(has_version(a_line)) > 0 :
            ## needs a certain version or not
            tmp_version_signs = has_version(a_line)
            if len(tmp_version_signs) == 1 and tmp_version_signs[0] == '=': tmp_version_signs.append("=")
            pkg_name, pkg_version = a_line.split(''.join(tmp_version_signs))
        else:
            pkg_name = a_line
            pkg_version = -1 
        
        not_found = True
        for b_line in files[args.input[1]]:
            if pkg_name in b_line:
                not_found = False
                found_pkgs+=1
                break
        if not_found: 
            return_exit_code = 1
            break
    if found_pkgs != len(files[args.input[1]]):
        return_exit_code = 1
    
    print("Comparison - Exit code  {}".format(return_exit_code))
    sys.exit(return_exit_code)

        
        

    #[ True for y in o_lines for x in ['=', '~', '>', '<'] if x in y]
