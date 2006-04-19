import difflib
from Globals import InitializeClass
from BaseDiff import BaseDiff, _getValue
from interfaces.portal_diff import IDifference


class FieldDiff(BaseDiff):
    """Text difference"""

    __implements__ = (IDifference)

    meta_type = "Field Diff"

    def _parseField(self, value):
        """Parse a field value in preparation for diffing"""
        # Since we only want to compare a single field, make a
        # one-item list out of it
        return [value]

    def getLineDiffs(self):
        a = self._parseField(self.oldValue)
        b = self._parseField(self.newValue)        
        return difflib.SequenceMatcher(None, a, b).get_opcodes()

    def testChanges(self, ob):
        """Test the specified object to determine if the change set will apply without errors"""
        value = _getValue(ob, self.field)
        if not self.same and value != self.oldValue:
            raise ValueError, ("Conflict Error during merge", self.field, value, self.oldValue)
        
    def applyChanges(self, ob):
        """Update the specified object with the difference"""
        # Simplistic update
        self.testChanges(ob)
        if not self.same:
            setattr(ob, self.field, self.newValue)

    def ndiff(self):
        """Return a textual diff"""
        r=[]
        a = self._parseField(self.oldValue)
        b = self._parseField(self.newValue)        
        for tag, alo, ahi, blo, bhi in self.getLineDiffs():
            if tag == 'replace':
                plain_replace(a, alo, ahi, b, blo, bhi, r)
            elif tag == 'delete':
                dump('-', a, alo, ahi, r)
            elif tag == 'insert':
                dump('+', b, blo, bhi, r)
            elif tag == 'equal':
                dump(' ', a, alo, ahi, r)
            else:
                raise ValueError, 'unknown tag ' + `tag`
        return '\n'.join(r)

InitializeClass(FieldDiff)

def dump(tag, x, lo, hi, r):
    for i in xrange(lo, hi):
        r.append(tag +' ' + str(x[i]))

def plain_replace(a, alo, ahi, b, blo, bhi, r):
    assert alo < ahi and blo < bhi
    # dump the shorter block first -- reduces the burden on short-term
    # memory if the blocks are of very different sizes
    if bhi - blo < ahi - alo:
        dump('+', b, blo, bhi, r)
        dump('-', a, alo, ahi, r)
    else:
        dump('-', a, alo, ahi, r)
        dump('+', b, blo, bhi, r)