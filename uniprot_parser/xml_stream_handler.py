"""
File: xml_stream_handler.py

A set of xml_stream_handler classes, which can process entries
extracted from an xml_parser. Each xml_stream_handler should inherit
from the base xml_stream_handler class.

Also contains a simple sequence_feature class, which stores sequence
feature attributes.

"""

class sequence_feature(object) :
  """
  A simple class to represent a sequence feature annotation.
  The begin_end_poss list stores start and stop coordinates
  in tuples: [(start1,stop1), (start2,stop2), ...]
  """
  def __init__(self) :
    self.description = '-'
    self.type = '-'
    self.begin_end_poss = []

class xml_stream_handler(object) :
  """
  Base class for handling XML streams. This could be implemented to either
  store the entries to a list or table, or to process the entries on the
  fly and write to a file. processEntry() is the main function that is
  called with each new entry read in.
  """

  def __init__(self) :
    self.entryCount = 0

  def processEntry(self, entry_lines) :
    """
    Process an entry from a list of lines
    """
    raise NotImplementedError('Base class XML stream handler'
      + ' does not implement processEntry()')

  def finalize(self) :
    """
    Return a value after the stream is complete
    """
    raise NotImplementedError('Base class XML stream handler'
      + ' does not implement finalize()')

class xml_stream_id_anot_seq(xml_stream_handler) :

  """
  A sub-interface of xml_stream_handler that gets id, anotations, and seq.
  Not a final class; provides an interface for storing these attributes.
  """

  def __init__(self) :
    super(xml_stream_id_anot_seq, self).__init__()

  def processEntry(self, entry_lines) :
    """
    Get the id, annotations, and sequence for this entry_set.
    Arugment: A list of lines for one entry
    Returns: a list of <id, annotation_set, seq)
    """

    _id = ''
    _seq = ''
    _annotation_set = []

    for line in entry_lines :
      l = line.strip()
      if len(l) > 11 and l[:11].strip() == '<accession>' :
        _id = l.split('>')[1].split('<')[0]
      elif len(l) > 9 and l[:9].strip() == '<sequence' :
        _seq = l.split('>')[1].split('<')[0]
      elif len(l) > 8 and l[:8] == '<feature' :
        cur_feature = sequence_feature()
        if 'description' in l :
          cur_feature.description = l[l.index('description'):].split('"')[1].replace(' ', '-')
        if 'type' in l :
          cur_feature.type = l[l.index('description'):].split('"')[1].replace(' ', '-')
      elif len(l) > 6 and l[:6] == '<begin' :
        cur_feature.begin_end_poss.append(int(l[l.index('position'):].split('"')[1]))
      elif len(l) > 4 and l[:4] == '<end' :
        cur_feature.begin_end_poss[-1] = 
          (cur_feature.begin_end_poss[-1], (int(l[l.index('position'):].split('"')[1])))
      elif len(l) > 9 and l[:9] == '</feature' :
        _annotation_set.append(cur_feature)

    self.storeIdAnotSeq(_id, _seq, _annotation_set)

  def storeIdAnotSeq(self,_id,_annotation_set,_seq) :
    """
    Should be handeled by subclass. Store or process the stripped
    id, annotations, and seq triple.
    """
    raise NotImplementedError('Base class xml_stream_id_anot_seq'
      + ' does not implement storeIdAnotSeq()')

class xml_id_annot_seq_to_file(xml_stream_id_anot_seq) :
  """
  An implementation of xml stream handler that writes a tsv file with
  id, annotations, and sequence. The file is normalized by sequence feature,
  so each <start, stop> pair of each sequence feature gets its own line
  in the output tsv file.
  """

  def __init__(self, filename) :
    super(xml_id_annot_seq_to_file, self).__init__()
    self.writer = open(filename, 'w')
    writer.write('')
    self.writer.write('%s\t%s\t%s\t%d\t%d\t%s\n' % 
      ('id', 'seq_feature.type', 'seq_feature.description', 'start', 'stop', 'seq'))

  def storeIdAnotSeq(self,_id,_annotation_set,_seq) :
    """
    Write this entry to the file. Treat each start/stop position
    pair as a seperate instance of the feature.
    """

    for seq_feature in _annotation_set :
      for (start,stop) in seq_feature.begin_end_poss :
        self.writer.write('%s\t%s\t%s\t%d\t%d\t%s\n' % 
          (_id, seq_feature.type, seq_feature.description, start, stop, _seq))

  def finalize(self) :
    self.writer.close()
