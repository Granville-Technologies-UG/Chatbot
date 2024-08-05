from fpdf import FPDF


class PDF(FPDF):
    def __init__(self):
        super().__init__()
        # Load Montserrat font
        self.add_font(
            "Montserrat-Bold",
            "",
            "../fonts/montserrat/fonts/ttf/Montserrat-Bold.ttf",
            uni=True,
        )
        self.add_font(
            "Montserrat-Regular",
            "",
            "../fonts/montserrat/fonts/ttf/Montserrat-Regular.ttf",
            uni=True,
        )
        self.add_font(
            "Montserrat-Italic",
            "",
            "../fonts/montserrat/fonts/ttf/Montserrat-Italic.ttf",
            uni=True,
        )

    def header(self):
        # Header
        self.set_font("Montserrat-Regular", "", 12)
        self.set_text_color(128)
        self.cell(0, 10, "NO. 000001", ln=True, align="R")
        self.ln(10)

    def footer(self):
        # footer
        self.set_y(-15)
        self.set_font("Montserrat-Italic", "", 10)
        self.set_text_color(128)
        self.cell(0, 10, "Thank you for booking with Tubayo!", 0, 0, "C")

    def invoice_body(self, user_info, booking_info):
        # Invoice title
        self.set_font("Montserrat-Bold", "", 44)
        self.set_text_color(0, 0, 0)
        self.cell(0, 10, "INVOICE", 0, 1, "L")
        self.ln(5)

        # Date
        self.set_font("Montserrat-Bold", "", 12)
        self.cell(0, 10, f"Date: {booking_info['date']}", 0, 1, "L")
        self.ln(5)

        # From and Billed To section
        self.set_font("Montserrat-Bold", "", 12)
        self.cell(95, 10, "From:", 0, 0)
        self.cell(95, 10, "Billed To:", 0, 1)
        self.set_font("Montserrat-Regular", "", 12)
        self.cell(95, 5, "Tubayo Travel Agency", 0, 0)
        self.cell(95, 5, f"{user_info['name']}", 0, 1)
        self.cell(95, 5, "travel@tubayo.com", 0, 0)
        self.cell(95, 5, f"{user_info['email']}", 0, 1)
        self.cell(95, 5, "+256 776823818", 0, 0)
        self.cell(95, 5, f"{user_info['phone']}", 0, 1)
        self.multi_cell(
            95,
            5,
            "Ntinda Complex, Ntinda, Kampala\nInnovation Village, Block D, Ground Floor",
            0,
            "L",
        )
        self.ln(10)

        # Table Header
        self.set_font("Montserrat-Bold", "", 12)
        self.set_fill_color(230, 230, 230)
        self.set_draw_color(200, 200, 200)
        self.cell(80, 10, "Category", 1, 0, "C", 1)
        self.cell(40, 10, "Details", 1, 0, "C", 1)
        self.cell(30, 10, "Quantity", 1, 0, "C", 1)
        self.cell(40, 10, "Total Cost", 1, 1, "C", 1)

        # Table Data
        self.set_font("Montserrat-Regular", "", 12)
        self.cell(80, 10, "Home", 1)
        self.cell(40, 10, booking_info["home"], 1)
        self.cell(30, 10, "1", 1)
        self.cell(40, 10, f"${booking_info['total_cost'] / 2:.2f}", 1, 1, "C")

        self.cell(80, 10, "Experience", 1)
        self.cell(40, 10, booking_info["experience"], 1)
        self.cell(30, 10, "1", 1)
        self.cell(40, 10, f"${booking_info['total_cost'] / 2:.2f}", 1, 1, "C")

        self.ln(5)
        self.set_font("Montserrat-Bold", "", 12)
        self.cell(80, 10, "", 0)
        self.cell(40, 10, "", 0)
        self.cell(30, 10, "Total:", 0)
        self.cell(40, 10, f"${booking_info['total_cost']:.2f}", 0, 1, "C")

        self.ln(5)
        self.set_font("Montserrat-Italic", "", 10)
        self.multi_cell(
            0,
            10,
            "Terms and Conditions:\n1. Payment is due within 30 days.\n2. Please contact us for any inquiries or issues with your booking.",
            0,
            "L",
        )
