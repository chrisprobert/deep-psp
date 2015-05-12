"""

File: xml_parser.py

A simple uniprot xml parser. Reads entries from the file, and uses an
xml_stream_handler object to store or process each entry.

"""

from subprocess import check_output

class xml_parser(object) :
  """
  The main XML parser class. Can read an XML file, and use a stream
  handler to store or process the file.

  """

  def __init__(self, stream_handler) :
    self.stream_handler = stream_handler

  def parse_xml_file(self, filename) :
    
    total_num_lines = int(check_output(['wc', '-l', filename]).strip().split()[0])
    line_count = 0
    print_every = 1000000

    def checkIfMatch(l, s) : return len(l) >= len(s) and l[:len(s)] == s

    cur_entry_lines = []

    for line in open(filename, 'r') :
      if line_count % print_every == 0 :
        print('processed %d/%d lines (%.1f)' %
          (line_count, total_num_lines, float(line_count)/total_num_lines))
      line_count += 1

      if checkIfMatch(line, '<entry') :
        if cur_entry_lines :
          self.stream_handler.processEntry(cur_entry_lines)
        cur_entry_lines = []

      cur_entry_lines.append(line)

    self.stream_handler.processEntry(cur_entry_lines)
    print('processed %d/%d lines (%.1f)' %
      (line_count, total_num_lines, float(line_count)/total_num_lines))

    self.stream_handler.finalize()
