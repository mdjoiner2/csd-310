# Name: Justin Morrow
# Team Green: Austin, Justin, Mark, and Tabari
# Date: 03/09/2025
# Assignment: CSD310 Module 12.2 "Bacchus Winery Mile Stone 5 - Updated based upon peer feedback"
# Updates include a user menu to choose printing options for the 3 reports.

import mysql.connector
from mysql.connector import errorcode
from dotenv import dotenv_values
from datetime import datetime
import tkinter as tk # added for tkinter functions
from tkinter import filedialog # added for windows save as pop-up box to save pdf reports
from fpdf import FPDF # added for report conversion to pdf
import matplotlib.pyplot as plt # used for the graph reports
import matplotlib as mpl # used for random colors on the bar graphs


# Load environment variables from the .env file
secrets = dotenv_values(".env")
config = {
    "user": secrets["USER"],
    "password": secrets["PASSWORD"],
    "host": secrets["HOST"],
    "database": secrets["DATABASE"],
    "raise_on_warnings": True
}

# Get current date and time for report generation
current_date_time = datetime.now()
formatted_date_time = current_date_time.strftime("%m-%d-%Y %I:%M:%S %p")


# This function will handle saving the report as a PDF and provide the pop-up window so user can choose location
# I reused this code from a project I worked on previously from continuing education certification at CNM
def save_report_to_pdf(report_data, report_type):
    root = tk.Tk()
    root.title("Save As")
    root.geometry("1x1")
    root.resizable(False, False)
    root.lift()
    root.attributes("-topmost", True)
    root.after_idle(root.attributes, "-topmost", False)
    default_file_name = (f"{report_type}.pdf")
    file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")],initialfile=default_file_name)

    if file_path:
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        # This sets the title of the report, font type, bold and size
        pdf.set_font("Arial", 'B', size=16)
        pdf.cell(0, 10, "Bracchus Winery Report", ln=True, align='C')
        pdf.ln(5)
        # This sets the body of the report, font type, bold and size
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, report_data)
        pdf.output(file_path)
        print(f"Your PDF Report was saved successfully at {file_path}")
    root.quit()
    root.destroy()


# This function will show the suppliers and supplier deliveries raw for the report
def suppliers_report(cursor):
    cursor.execute("""
        SELECT supplier_deliveries.delivery_id, suppliers.supplier_name, supplier_deliveries.item_type, 
               supplier_deliveries.expected_delivery_date, supplier_deliveries.actual_delivery_date, 
               supplier_deliveries.quantity_delivered
        FROM supplier_deliveries
        JOIN suppliers ON supplier_deliveries.supplier_id = suppliers.supplier_id
    """)
    deliveries = cursor.fetchall()

    # Format the data into a string for the report
    report_data = f"\n\nDelivery Schedule Report     |     Generated on: {formatted_date_time}\n\n"
    for delivery in deliveries:
        report_data += f"\nDelivery ID: {delivery[0]}\n"
        report_data += f"Supplier Name: {delivery[1]}\n"
        report_data += f"Item Type: {delivery[2]}\n"
        report_data += f"Expected Delivery Date: {delivery[3]}\n"
        report_data += f"Actual Delivery Date: {delivery[4]}\n"
        expected_delivery_date = delivery[3]
        actual_delivery_date = delivery[4]
        if actual_delivery_date == expected_delivery_date:
            report_data += "Shipment Delivery: On time\n"
        else:
            report_data += "Shipment Delivery: Was late\n"
        report_data += f"Quantity Delivered: {delivery[5]:,.0f}\n\n"
    report_data += "\nAll Rights Reserved by: Bellevue University CSD 310 Green Team: Austin, Justin, Mark and Tabari.\n\n"

    # Return both the formatted and raw data to the employees report
    return report_data, deliveries


# This function will be used to show the distributors and wine_sales raw data as a report if the user selects option # 2
def distributors_report(cursor):
    cursor.execute("""
        SELECT wine_grape_variety.wine_name, distributors.distributor_name, wine_sales.sales_quantity, wine_sales.sale_date, wine_sales.price_per_unit
        FROM wine_sales
        JOIN wine_grape_variety ON wine_sales.product_id = wine_grape_variety.product_id
        JOIN distributors ON wine_sales.distributor_id = distributors.distributor_id
    """)
    wine_sales = cursor.fetchall()

    # Format the data into a string for the report
    report_data = f"\n\nWine Sales Report     |     Generated on: {formatted_date_time}\n\n"
    for sale in wine_sales:
        report_data += f"\nWine Name: {sale[0]}\n"
        report_data += f"Distributor: {sale[1]}\n"
        report_data += f"Sales Quantity: {sale[2]:,.0f}\n"
        report_data += f"Sale Date: {sale[3]}\n"
        report_data += f"Price per Unit: ${sale[4]:,.2f}\n"
        total_sales = sale[2] * sale[4]  # Calculation of Sales Quantity (Bottles sold) * Price per Unit (Cost of each bottle)
        report_data += f"Total Sales: ${total_sales:,.2f}\n"
    report_data += "\nAll Rights Reserved by: Bellevue University CSD 310 Green Team: Austin, Justin, Mark and Tabari.\n\n"

    # Return both the formatted and raw data to the employees report
    return report_data, wine_sales


# This function will be used to show the employees data and quarterly hours worked as a report. User selects option # 3
"""
Resource: Stack Overflow. (2021, February 4). SQL query: Calculate quarterly data from monthly data. Stack Overflow.
https://stackoverflow.com/questions/65797029/sql-query-calculate-quarterly-data-from-monthly-data
Stack Overflow. (2019, April 23). How to use SUM(CASE WHEN THEN) properly? Stack Overflow.
https://stackoverflow.com/questions/55812411/how-to-use-sum-case-when-then-properly
Stack Overflow. (2021, October 26). How to do grouping by multiple columns in MySQL SELECT statement? Stack Overflow.
https://stackoverflow.com/questions/69727154/how-to-do-grouping-by-multiple-columns-in-mysql-select-statement
"""
# This function will be used to show the employees data and quarterly hours worked as a report
def employees_report(cursor):
    # This will return the raw data (not formatted)
    cursor.execute("""
        SELECT employees.employee_id, employees.first_name, employees.last_name, employees.position,
               SUM(CASE WHEN time_card.month IN (1, 2, 3) THEN time_card.hours_worked ELSE 0 END) AS Q1_total_hours,
               SUM(CASE WHEN time_card.month IN (4, 5, 6) THEN time_card.hours_worked ELSE 0 END) AS Q2_total_hours,
               SUM(CASE WHEN time_card.month IN (7, 8, 9) THEN time_card.hours_worked ELSE 0 END) AS Q3_total_hours,
               SUM(CASE WHEN time_card.month IN (10, 11, 12) THEN time_card.hours_worked ELSE 0 END) AS Q4_total_hours
        FROM employees
        JOIN time_card ON employees.employee_id = time_card.employee_id
        GROUP BY employees.employee_id, employees.first_name, employees.last_name, employees.position
    """)
    employees = cursor.fetchall()

    # Format the data into a string for the report
    report_data = f"\n\nEmployee Worked Hours Report    |     Generated on: {formatted_date_time}\n\n"
    for employee in employees:
        report_data += f"\nEmployee ID: {employee[0]}\n"
        report_data += f"First Name: {employee[1]}\n"
        report_data += f"Last Name: {employee[2]}\n"
        report_data += f"Position: {employee[3]}\n"
        report_data += f"Q1 Total Hours Worked: {employee[4]:,.2f}\n"
        report_data += f"Q2 Total Hours Worked: {employee[5]:,.2f}\n"
        report_data += f"Q3 Total Hours Worked: {employee[6]:,.2f}\n"
        report_data += f"Q4 Total Hours Worked: {employee[7]:,.2f}\n"
    report_data += "\nAll Rights Reserved by: Bellevue University CSD 310 Green Team: Austin, Justin, Mark and Tabari.\n\n"

    # Return both the formatted and raw data to the employees report
    return report_data, employees


# This new function will give the user print options based upon peer feedback of using better visuals
def print_options(report_data, report_type, raw_data=None):
    print("\nChoose a print option:")
    print("1) Print to screen")
    print("2) Print to PDF")
    print("3) View as a Graph")
    print("4) Cancel Print")

    print_option = input("\nEnter your choice: ")
    if print_option == "1":
        print(report_data)  # Print the raw data to the screen
    elif print_option == "2":
        save_report_to_pdf(report_data,report_type)  # Run the save_report_to_pdf function to convert raw data to PDF and save as
    elif print_option == "3":
        print("View as a Graph in progress")
        if raw_data:
            generate_graph(raw_data, report_type)  # Pass the data to the graph function
    elif print_option == "4":
        print("\nYou selected to 'Cancel Printing'. Now returning to the report selection menu.\n")
    else:
        print("\nYou selected an invalid option, please try again by selecting options 1-4. Thank you.\n")


# New function in progress to generate a graph for each of the 3 reports per peer feedback on previous version
# Special thanks to my friend Connor Harness that helped me with the generate_graph setup
def generate_graph(raw_data, report_type):
    # Concatenate Supplier Name, Item Type and Expected Delivery Date at bottom of graph. Then determine if on-time/late
    if report_type == "Suppliers and Delivery Schedule Report":
        suppliers_items_date = [f"{row[1]}: {row[2]} ({row[3]})" for row in raw_data]
        quantities = [row[5] for row in raw_data]
        expected_dates = [row[3] for row in raw_data]
        actual_dates = [row[4] for row in raw_data]
        delivery_status = [1 if actual == expected else 0 for expected, actual in zip(expected_dates, actual_dates)]

        # Set up the figure and axis as well as the positioning, size and colors, and titles
        colors = ['green' if status == 1 else 'red' for status in delivery_status]
        plt.figure(figsize=(10, 6))
        plt.bar(suppliers_items_date, quantities, color=colors)
        plt.xlabel('Supplier Name: Item Type (Expected Delivery Date)')
        plt.ylabel('Quantity Delivered')
        plt.title('Supplier On-Time/Late Delivery Report')

        # Add a legend for On Time being green and Late being red
        from matplotlib.patches import Patch
        legend_elements = [Patch(color='green', label='On Time'), Patch(color='red', label='Late')]
        plt.legend(handles=legend_elements)

        # Rotate and tighten the bottom X axis labels to display better since longer from join/concatenation
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

    # Concatenated Wine name, Distributor name, Sales Quantity and Date sold to determine Wine Sales/Performance
    elif report_type == "Distributors and Wine Sales Report":
        wine_distributor_sales = [f"{row[0]}: {row[1]} ({row[2]:,.0f} | Date: {row[3]})" for row in raw_data]
        total_sales = [row[2] * row[4] for row in raw_data]

        # Set up the figure and axis as well as the positioning, size and colors for each quarterly bar for each employee
        num_bars = len(raw_data)
        colors = mpl.colormaps['tab20'](range(num_bars))
        plt.figure(figsize=(12, 6))
        plt.bar(wine_distributor_sales, total_sales, color=colors)
        plt.xlabel('Wine Name: Distributor (Sales Quantity) | Date')
        plt.ylabel('Total Sales ($)')
        plt.title('Wine Sales Report by Distributor and Date')

        # Rotate and tighten the bottom X axis labels to display better since longer from join/concatenation
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

    # Concatenate first and last name for rows 1 and 2 and job title for row 3 and map the Q1 - Q4 hours to the rows
    elif report_type == "Employee Hours Worked Report":
        employees = [f"{row[1]}: {row[2]} ({row[3]})" for row in raw_data]
        q1_hours = [row[4] for row in raw_data]
        q2_hours = [row[5] for row in raw_data]
        q3_hours = [row[6] for row in raw_data]
        q4_hours = [row[7] for row in raw_data]

        # Set up the figure and axis as well as the positioning, size and colors for each quarterly bar for each employee
        fig, ax = plt.subplots(figsize=(10, 6))
        bar_width = 0.2
        index = range(len(employees))
        bar_positions_q1 = [i - 1.5 * bar_width for i in index]
        bar_positions_q2 = [i - 0.5 * bar_width for i in index]
        bar_positions_q3 = [i + 0.5 * bar_width for i in index]
        bar_positions_q4 = [i + 1.5 * bar_width for i in index]
        ax.bar(bar_positions_q1, q1_hours, bar_width, label="Q1", color='tab:blue')
        ax.bar(bar_positions_q2, q2_hours, bar_width, label="Q2", color='tab:orange')
        ax.bar(bar_positions_q3, q3_hours, bar_width, label="Q3", color='tab:green')
        ax.bar(bar_positions_q4, q4_hours, bar_width, label="Q4", color='tab:red')

        # Rotate and tighten the bottom X axis labels to display better since longer from join/concatenation
        # Set report titles. Rotate/tighten bottom X axis labels to display better since longer from joins/concatenation
        ax.set_xlabel('Employee Name (Employee Title)')
        ax.set_ylabel('Total Hours Worked')
        ax.set_title('Employee Hours Worked by Quarter Report')
        ax.set_xticks(index)
        ax.set_xticklabels(employees, rotation=45, ha="right")
        ax.legend()
        plt.tight_layout()
        plt.show()


# Main function to handle user input and generate the appropriate report
def main():
    try:
        db = mysql.connector.connect(**config)
        cursor = db.cursor()

        print("\nWelcome to the Bacchus Winery Report Tool")

        # Display the main menu for the user to select a report or quit the program
        while True:
            print("\nPlease select a report to generate:")
            print("1) Suppliers and Delivery Schedule Report")
            print("2) Distributors and Wine Sales Report")
            print("3) Employee Hours Worked Report")
            print("Q) Quit")

            choice = input("\nEnter the number of your choice to display the report: ")

            # Option 1 will print the Suppliers Report with the formatted and raw data
            if choice == "1":
                suppliers_report_data, suppliers_raw_data = suppliers_report(cursor)
                report_type = "Suppliers and Delivery Schedule Report"
                print_options(suppliers_report_data, report_type, raw_data=suppliers_raw_data)
            # Option 2 will print the Distributors Report with the formatted and raw data
            elif choice == "2":
                distributors_report_data, distributors_raw_data = distributors_report(cursor)
                report_type = "Distributors and Wine Sales Report"
                print_options(distributors_report_data, report_type, raw_data=distributors_raw_data)
            # Option 3 will print the Employees Report with the formatted and raw data
            elif choice == "3":
                employee_hours_report_data, employees_raw_data = employees_report(cursor)
                report_type = "Employee Hours Worked Report"
                print_options(employee_hours_report_data, report_type, raw_data=employees_raw_data)
            # The 4th option is Q to quit the program
            elif choice.upper() == "Q":
                print("\nThe database connection will now automatically disconnect...")
                break
            # This is the Error handling else option if the user enters an incorrect option
            else:
                print("\nInvalid choice. Please enter a number: 1-3 to view a report, or Q to Quit.\n")

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("The supplied username or password are invalid.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("The specified database does not exist.")
        else:
            print(err)

    finally:
        db.close()


if __name__ == "__main__":
    main()
