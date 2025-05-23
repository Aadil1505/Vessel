import os
import json
import logging

def analyze_react_project(project_path):
    """
    Analyze a plain React project and gather information about its structure.
    
    Args:
        project_path (str): Path to the React project
        
    Returns:
        dict: Project information or None if not a valid React project
    """
    # Check for package.json
    package_json_path = os.path.join(project_path, 'package.json')
    if not os.path.exists(package_json_path):
        return None
    
    # Parse package.json
    try:
        with open(package_json_path, 'r') as f:
            package_data = json.load(f)
            
        # Check if it's a React project
        dependencies = package_data.get('dependencies', {})
        dev_dependencies = package_data.get('devDependencies', {})
        
        if 'react' not in dependencies and 'react' not in dev_dependencies:
            return None
            
        # Gather basic project info
        project_info = {
            'name': package_data.get('name', 'react-app'),
            'path': project_path,
            'dependencies': dependencies,
            'dev_dependencies': dev_dependencies,
            'scripts': package_data.get('scripts', {}),
        }
        
        # Determine build command and output directory
        if 'build' in project_info['scripts']:
            project_info['build_command'] = 'npm run build'
            project_info['build_output'] = 'build'  # Standard CRA output directory
        else:
            # No build script found
            project_info['build_command'] = 'npm run build'  # Default
            project_info['build_output'] = 'build'  # Default
            
        return project_info
        
    except Exception as e:
        logging.error(f"Error analyzing project: {str(e)}")
        return None