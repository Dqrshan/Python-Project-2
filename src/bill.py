import csv
import tkinter.messagebox as box


def bill(cursor):
    cursor.execute('SELECT curdate() FROM dual')
    date = cursor.fetchone()
    cursor.execute('SELECT curtime() FROM dual')
    traw = cursor.fetchone()
    t = str(traw[0]).split(':')
    time = "".join(t)
    file = open(fr'.\bills\bill-{date[0]}-{time}.csv', 'w')
    writer = csv.writer(file)
    cursor.execute('SELECT * FROM Shop')
    writer.writerow([f'Bill {date[0]} {traw[0]}'])
    writer.writerow(['Item ID', 'Name', 'Price'])
    total = 0
    for i in cursor.fetchall():
        writer.writerow(i)
        total += i[2]
    writer.writerow(['', '', ''])
    writer.writerow(['Total:', '', str(total)])
    file.close()
    box.showinfo('Bill Generated!',
                 f'Successfully generated bill!\n\tDate: {date[0]}\n\tTime: {traw[0]}\n\nPlease check the "bills" folder!')
