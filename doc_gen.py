from docxtpl import DocxTemplate
from docx2pdf import convert


def generate_selling_bill(invoice_list, detail_dict):
    try:
        doc = DocxTemplate("Morya Electronics.docx")
        doc.render({'name': detail_dict['name'],
                    'address':detail_dict['address'],
                    'number':detail_dict['number'],
                    'gst_number':detail_dict['gst_number'],
                    'bill_no':detail_dict['bill_no'],
                    'today_date':detail_dict['today_date'],
                    'payment_mode':detail_dict['payment_mode'],
                    'bank_details':detail_dict['bank_details'],
                    'total':detail_dict['total'],
                    'total_discount':detail_dict['total_discount'],
                    'taxable_amt':detail_dict['taxable_amt'],
                    'cgst':detail_dict['cgst'],
                    'sgst':detail_dict['sgst'],
                    'cgst_per':detail_dict['cgst_per'],
                    'sgst_per':detail_dict['sgst_per'],
                    'round_off':detail_dict['round_off'],
                    'grand_total':detail_dict['grand_total'],
                    'amount_in_words':detail_dict['amount_in_words'],
                    'total_items':detail_dict['total_items'],
                    'invoice_list':invoice_list})
        doc.save('New_Invoice.docx')
        return True
    except:
        return False


def generate_qr_bill(selling_price, mrp, discount):
    try:    
        doc = DocxTemplate('qr_template.docx')
        doc.replace_pic('image1.png','refresh.png')
        doc.replace_pic('image1.png','refresh.png')
        doc.render({"selling_price":selling_price, 'mrp':mrp, 'discount':discount})
        doc.save('New_Invoice.docx')
        convert("New_Invoice.docx")
        convert("input.docx", "output.pdf")
        return True
    except :
        return False


# print(generate_qr_bill('qr_template.docx'))

# invoice_list = [
#     ['1', '567TGBJW89J', 'Air conditioner', 'LG 3 star 1.5 ton smart ac top open', '19000', '3000', '16000'],
#     ['2', 'QW1212490IE', 'Washing machine', 'Hyundai 10kg side bar machine 5 star LL093', '18000', '2100', '15900'],
#     ['3', 'QTE312490IE', 'Washing machine', 'Hyundai 25kg side bar machine 5 star LL093', '18000', '2100', '15900']]

# detail_dict = {
#     'name': '',
#     'address':'',
#     'number':'',
#     'gst_number':'',
#     'bill_no':'',
#     'today_date':'',
#     'payment_mode':'',
#     'bank_details':'',
#     'total':'',
#     'total_discount':'',
#     'taxable_amt':'',
#     'cgst':'',
#     'sgst':'',
#     'cgst_per':'',
#     'sgst_per':'',
#     'round_off':'',
#     'grand_total':'',
#     'amount_in_words':'',
#     'total_items':'',
#     }