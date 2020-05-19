from graphviz import Source

s = Source.from_file('fboaventuradev_terraform.dot', format='png')
s.save(filename='fboaventuradev_tf')
s.view()
