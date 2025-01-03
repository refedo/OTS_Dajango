import os
from django.core.management.base import BaseCommand
import pandas as pd

class Command(BaseCommand):
    help = 'Creates an Excel template for raw data import'

    def handle(self, *args, **kwargs):
        # Define the columns with example data
        data = {
            'building_name': ['Building A', 'Building A', 'Building B', 'Building B'],
            'log_designation': ['LOG-001', 'LOG-001', 'LOG-002', 'LOG-002'],
            'part_designation': ['Assembly Part', 'Single Part', 'Assembly Part', 'Assembly Part'],
            'assembly_mark': ['BM1', 'BM1-1', 'COL1', 'BR1'],
            'part_mark': ['BM1-A', 'PL1', 'COL1-A', 'BR1-A'],
            'name_designation': ['Beam', 'Plate', 'Column', 'Bracing'],
            'quantity': [1, 2, 1, 1],
            'profile': ['IPE300', 'PL10', 'HEA200', 'L100x100x10'],
            'grade': ['S275JR', 'S275JR', 'S275JR', 'S275JR'],
            'length': [6000, 200, 4000, 3500],
            'net_area_single': [7.5, 0.02, 5.0, 2.5],
            'net_area_total': [7.5, 0.04, 5.0, 2.5],
            'single_part_weight': [220.5, 1.57, 150.8, 45.2],
            'net_weight_total': [220.5, 3.14, 150.8, 45.2],
            'revision': ['R0', 'R0', 'R0', 'R0']
        }

        # Create DataFrame
        df = pd.DataFrame(data)

        # Define the output path
        output_path = os.path.join('static', 'templates', 'raw_data_import_template.xlsx')

        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Create Excel writer object
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Write the template sheet
            df.to_excel(writer, sheet_name='Template', index=False)
            
            # Get the workbook and the template worksheet
            workbook = writer.book
            worksheet = writer.sheets['Template']
            
            # Add a new sheet with instructions
            instructions = workbook.create_sheet('Instructions', 0)
            
            # Add instructions
            instructions.append(['Raw Data Import Instructions'])
            instructions.append([''])
            instructions.append(['1. Use the Template sheet for your data'])
            instructions.append(['2. All columns are required'])
            instructions.append(['3. Follow the data format shown in the example rows'])
            instructions.append(['4. Building names can be any unique identifier (e.g., A1, Block B, Tower 1)'])
            instructions.append(['5. Numeric values should not contain units'])
            instructions.append(['6. Do not change column names'])
            instructions.append(['7. Save as .xlsx or .csv before uploading'])

            # Format the instructions
            for row in instructions:
                instructions.append(row)

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created template at {output_path}')
        )
