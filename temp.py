a = ['foo', 'qux']
b = ['foo', 'bar', 'baz']
c = ['foo', 'bar', 'qux']
# print set(a)
# print set(b)

print set(a) in set(c)
#
# if set(a) <= set(b):
#     print "a is in b"
# if set(a) <= set(c):
#     print 'a is in c'
# # else:
# #     print 'a is not in b'


for business in businesses:
    for category in business_categories:  # O (N)
        if category in match_categories:  # O (N)
            i += 1