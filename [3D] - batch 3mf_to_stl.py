import os
import sys
import argparse
import pymesh
import meshio


print("None of the above libraries can open 3MF so writing a script is useless.  \nJust search for \"Spin 3D Mesh Convertor\" and use that. \nIt can do batch 3MF-> STL or OBJ")
# def convert_files(input_dir):
#     # Check if input directory exists
#     if not os.path.exists(input_dir):
#         print(f"Directory '{input_dir}' does not exist.")
#         return

#     # Get all 3MF files in the directory
#     files = [f for f in os.listdir(input_dir) if f.endswith('.3mf')]

#     # Convert each 3MF file to STL
#     for file in files:
#         input_path = os.path.join(input_dir, file)
#         output_path = os.path.splitext(input_path)[0] + '.stl'
#         mesh = pymesh.load_mesh(input_path)
#         pymesh.save_mesh(output_path, mesh)
#         print(f"Converted '{input_path}' to '{output_path}'.")
        
#         # Set output file permissions to match input file permissions
#         input_stat = os.stat(input_path)
#         os.chmod(output_path, input_stat.st_mode)

# if __name__ == '__main__':
#     # Parse command line arguments
#     parser = argparse.ArgumentParser(description='Convert 3MF files to STL files.')
#     parser.add_argument('input_dir', help='Input directory.')
#     args = parser.parse_args()

#     # Convert files in input directory
#     convert_files(args.input_dir)
