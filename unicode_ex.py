# Python ascii codec can't decode and unicode mess
#
# check this out https://pythonhosted.org/kitchen/unicode-frustrations.html
# and this http://www.joelonsoftware.com/articles/Unicode.html
#
# The short of it is this
# 1. If you can, always set PYTHONIOENCODING=utf8 before you start your python programs.
# 2. If you can't or you can't ensure this, always use the following lambda _u to get unicode text
#    whereever you convert to strings (str.format, str % etc.)
#
# So for 2. you always do this:
# _u = lambda t: t.decode('UTF-8', 'replace') if isinstance(t, str) else t
# _uu = lambda *tt: tuple(_u(t) for t in tt)
# # use like this
# text='Some string with codes > 127, like Zürich'
# print "Some unknown input %s" % _u(text)
# print "Multiple inputs %s, %s" % _uu(text, text)
# # or like this
# print u"Some string with codecs > 127 {}".format(_u(text))
# print u"Multiple inputs {}, {}".format(_uu(text, text))
# ---
# amazingly, you can assign UTF8 to strings, it works nicely
print "==> We'll work with these strings"
text = "Zürich"
utext = u"Zürich"
print text, type(text)
print utext, type(utext)
# will raise UnicodeDeocdeError
try:
    print "==> Try as unicode(text) => error"
    print unicode(text)
except UnicodeDecodeError as e:
    print e
# try again
print "==> Try as with replacing unknown characters"
print unicode(text, errors="replace")
# again
print "==> Try as with ignoring unknown characters"
print unicode(text, errors='ignore')
# again
print "==> Try as with UTF-8 encoding"
print unicode(text, encoding="UTF-8")
# but this doesn't work!!
try:
    print "But amazingly you can't encode unicode ext into UTF8"
    print unicode(utext, encoding="UTF-8")
except Exception as e:
    print "because %s" %e
# be smart
print "==> So you want unicode in string formats, huh?"
try:
    print u"%s" % text
except UnicodeDecodeError as e:
    print "Not so fast! %s" % e
# let's try that again
print "==> Now for real using string formats"
print u"%s" % unicode(text, 'UTF-8')
# so you think that's taking all the fun out of working with string formatting?
print "==> Doing it like this works more naturally"
print unicode("%s" % text, 'UTF-8')
try:
    print "==> except if the string is already unicode:"
    print unicode("%s" % utext, 'UTF-8')
except Exception as e:
    print "sorry, no can do, %s" % e
# can we join, slice etc. such strings?
otext = "ü".join(text)
print otext
# even better, use export PYTHONIOENCODING=utf8, if you can at start up time
# see http://stackoverflow.com/a/27066059/890242
#---------
# let's deal with unicode itself
print "===> Unicode text can just be printed like that, because they are of type unicode"
print "%s" % utext, type("%s" % utext)
# but if you combine the two, the fun starts
print "===> Unicode + byte text cannot just be printed like that, because they are of type unicode"
try:
    print "%s == %s" % (utext, text), type("%s" % utext)
except UnicodeDecodeError as e:
    print "because, well, %s" % e
# try again
print "===> But you can covert them all to unicode or UTF8"
print unicode("%s == %s" % (utext, unicode(text, 'UTF-8')))
print "%s == %s" % (utext, unicode(text, 'UTF-8'))
try:
    print "%s == %s" % (utext.decode('UTF-8'), text.decode('UTF-8'))
except UnicodeDecodeError as e:
    print "no so fast... %s" % e
except Exception as e:
    print "no so fast... %s" % e
# again
print "===> byte strings with codes > 127 are harder. You have to DECODE to utf8"
print text.decode('UTF-8')
try:
    print text.encode('UTF-8')
except Exception as e:
    print "because encode won't work, %s" % e
print "===> while you have to ENCODE unicodes. You can't decode unicode into UTF-8."
print "works:", utext.encode('UTF-8')
try:
    print "doesn't:", utext.decode('UTF-8')
except Exception as e:
     print "%s" % e
# in summary, if you know you want
print "==> So in summary, always use unicode(text, 'UTF-8') to ensure you have unicode text from byte code"
print unicode(text, 'UTF-8')
print "==> or save-get a unicode object from your inputs, whether unicode or byte string"
_u = lambda t: t.decode('UTF-8', 'replace') if isinstance(t, str) else t
#else unicode(text.encode('UTF-8', 'replace'))
print _u(text), type(_u(text))
print _u(utext), type(_u(utext))
print "==> then you can mix match safely"
text = _u(text)
print "%s == %s" % (text, utext)
print u"%s == %s" % (text, utext)
# Conclusion: Always use this:
# guarantee unicode
_u = lambda t: t.decode('UTF-8', 'replace') if isinstance(t, str) else t
_uu = lambda *tt: tuple(_u(t) for t in tt)
# guarantee byte string in UTF8
_u8 = lambda t: t.encode('UTF-8', 'replace') if isinstance(t, unicode) else t
_uu8 = lambda *tt: tuple(_u8(t) for t in tt)
text='Some string with codes > 127, like Zürich'
print "==> with _u, _uu"
print _u(text), type(_u(text))
print _u(utext), type(_u(utext))
print _uu(text, utext), type(_uu(text, utext))
print "==> with u8, uu8"
print _u8(text), type(_u8(text))
print _u8(utext), type(_u8(utext))
print _uu8(text, utext), type(_uu8(text, utext))
# with % formatting, always use _u() and _uu()
print "Some unknown input %s" % _u(text)
print "Multiple inputs %s, %s" % _uu(text, text)
# but with .format be sure to always work with unicode strings
print u"Also works with formats: {}".format(_u(text))
print u"Also works with formats: {},{}".format(*_uu(text, text))
# ... or use _u8 and _uu8, because string.format expects byte strings
print "Also works with formats: {}".format(_u8(text))
print "Also works with formats: {},{}".format(*_uu8(text, text))