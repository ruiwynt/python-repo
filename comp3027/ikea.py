from email.utils import encode_rfc2231
from errno import EFAULT


def read_sequence(i):
    """This helper function reads i lines as i products or boxes
    They are returned as a list of tuples like [("p1", 2, 4), ("p2", 5, 3), ...]
    (You may replace this representation with something else if you want.)
    """
    sequence = []
    for _ in range(i):
        name, x, y = input().split()
        sequence.append((name, int(x), int(y)))
    return sequence

# boxes = [('b1', 253, 426), ('b2', 828, 478), ('b3', 314, 226), ('b4', 282, 716), ('b5', 500, 858), ('b6', 171, 165), ('b7', 246, 306), ('b8', 148, 707), ('b9', 984, 583), ('b10', 854, 381), ('b11', 264, 624), ('b12', 720, 512), ('b13', 136, 571), ('b14', 506, 140), ('b15', 147, 419), ('b16', 351, 894), ('b17', 134, 605), ('b18', 877, 924), ('b19', 663, 751), ('b20', 513, 900), ('b21', 852, 457), ('b22', 250, 186), ('b23', 670, 227), ('b24', 300, 317), ('b25', 347, 713), ('b26', 962, 736), ('b27', 224, 291), ('b28', 764, 557), ('b29', 586, 613), ('b30', 335, 816), ('b31', 336, 204), ('b32', 567, 913), ('b33', 965, 983), ('b34', 823, 467), ('b35', 417, 684), ('b36', 163, 750), ('b37', 185, 997), ('b38', 521, 892), ('b39', 225, 831), ('b40', 719, 795), ('b41', 142, 263), ('b42', 220, 375), ('b43', 888, 749), ('b44', 959, 814), ('b45', 647, 608), ('b46', 627, 112), ('b47', 856, 231), ('b48', 255, 209), ('b49', 659, 681), ('b50', 441, 445), ('b51', 928, 809), ('b52', 374, 657), ('b53', 193, 922), ('b54', 827, 103), ('b55', 510, 318), ('b56', 944, 434), ('b57', 535, 397), ('b58', 863, 612), ('b59', 293, 369), ('b60', 601, 946), ('b61', 542, 230), ('b62', 468, 123), ('b63', 970, 870), ('b64', 327, 137)]
# products = [('p1', 365, 498), ('p2', 748, 308), ('p3', 119, 402), ('p4', 692, 525), ('p5', 235, 638), ('p6', 677, 450), ('p7', 358, 387), ('p8', 455, 912), ('p9', 392, 842), ('p10', 796, 469), ('p11', 188, 229), ('p12', 243, 116), ('p13', 333, 957), ('p14', 806, 834), ('p15', 412, 278), ('p16', 797, 644), ('p17', 927, 975), ('p18', 917, 672), ('p19', 874, 943), ('p20', 635, 969), ('p21', 144, 159), ('p22', 757, 899), ('p23', 538, 582), ('p24', 393, 501), ('p25', 802, 385), ('p26', 212, 689), ('p27', 356, 307), ('p28', 712, 906), ('p29', 662, 143), ('p30', 971, 755), ('p31', 292, 830), ('p32', 801, 215), ('p33', 503, 354), ('p34', 473, 723), ('p35', 302, 304), ('p36', 241, 574), ('p37', 110, 886), ('p38', 405, 465), ('p39', 746, 175), ('p40', 811, 341), ('p41', 793, 812), ('p42', 838, 996), ('p43', 706, 545), ('p44', 287, 141), ('p45', 594, 979), ('p46', 284, 575), ('p47', 305, 528), ('p48', 111, 762), ('p49', 592, 415), ('p50', 114, 935), ('p51', 745, 294), ('p52', 884, 632), ('p53', 157, 156), ('p54', 611, 666), ('p55', 158, 146), ('p56', 508, 800), ('p57', 197, 403), ('p58', 400, 153), ('p59', 730, 671), ('p60', 359, 233), ('p61', 774, 966), ('p62', 560, 254), ('p63', 604, 217), ('p64', 686, 372)]

boxes = [('b52', 374, 657), ('b35', 417, 684)]
products = [('p1', 365, 498), ('p24', 393, 501), ('p9', 392, 842), ('p58', 400, 153), ('p15', 412, 278), ('p38', 405, 465)]

############################
# write your solution here #
############################

# macros, for readability
length = lambda x: x[1]
width = lambda x: x[2]

# return total fit, preprocessing and start divide and conquer
def totalfit(products, boxes):
    products = sorted(products, key=width)
    boxes = sorted(boxes, key=width)
    return totalfit_recurse(products, boxes)

def get_median(arr):
    arr_c = sorted(arr)
    mid = (len(arr_c)-1)//2
    if len(arr) % 2 == 0:
        median = (arr_c[mid] + arr_c[mid+1])/2
    else:
        median = arr_c[mid]
    return median

def sorted_insert(src, target):
    i = 0
    j = 0
    while i < len(src):
        if j == len(target):
            target.append(src[i])
        else:
            while j < len(target) and width(src[i]) > width(target[j]):
                j += 1
            if j == len(target):
                target.append(src[i])
            else:
                target.insert(j, src[i])
        i += 1
            
def distribute_median(al, ar, am):
    if len(am) > 0:
        aml = []
        amr = []
        diff = abs(len(ar) - len(al))
        cutoff = min(len(am), diff)
        if len(ar) > len(al):
            aml = am[:cutoff]
        else:
            amr = am[:cutoff]
        am = am[cutoff:]
        while len(am) > 0:
            if len(aml) > len(amr):
                amr.append(am.pop(0))
            else:
                aml.append(am.pop(0))
        sorted_insert(al, aml) 
        sorted_insert(ar, amr) 
        return aml, amr
    return al, ar

def split_median(arr, d):
    al = [a for a in arr if length(a) < d]
    ar = [a for a in arr if length(a) > d]
    am = [a for a in arr if length(a) == d]
    al, ar = distribute_median(al, ar, am)
    return al, ar

def verify_width_order(arr):
    for i in range(1, len(arr)):
        if width(arr[i]) < width(arr[i-1]):
            print(arr)
            raise ValueError(f"Order was not maintained from element {i-1}: {arr[i-1]} to element {i}: {arr[i]}")

# recursion function (divide)
def totalfit_recurse(products, boxes):
    """
    Divide until length of "products" and "boxes" are both either length 1 or 0,
    then solve the base case and use combine to return subproblem solution.

    Assume that products and boxes are sorted by width already.
    Assume that for some D, the length of all items in products or boxes are <= D.
    """
    verify_width_order(products)
    verify_width_order(boxes)
    # Base cases
    if len(products) == 0 or len(boxes) == 0:
        return 0
    elif len(products) == 1 and len(boxes) == 1:
        if width(products[0]) <= width(boxes[0]) and length(products[0]) <= length(boxes[0]):
            return 1
        else:
            return 0

    if len(boxes) > 1:
        d = get_median(list(map(length, boxes)))
    elif len(products) > 1:
        d = get_median(list(map(length, products)))

    bl, br = split_median(boxes, d)
    pl, pr = split_median(products, d)

    fl = totalfit_recurse(pl, bl)
    fr = totalfit_recurse(pr, br)
    fcross = combine(pl, pr, bl, br)

    """
    fbrute = brute_fits(pl + pr, bl + br)
    efl = brute_fits(pl, bl)
    efr = brute_fits(pr, br)
    ftot = fl + fr + fcross
    if fbrute != ftot:
        print("OUTPUT WAS NOT THE SAME")
        print(f"expected: {fbrute}\t actual: {ftot}")
        print(f"bl: {bl}\t br: {br}")
        print(f"pl: {pl}\t pr: {pr}")
        print(f"fl: {fl}\t fr: {fr}\t fross: {fcross}")
        print(f"expected fl: {efl}, expected fr = {efr}, expected fcross: {fbrute - efl - efr}")
        print("")
    """

    return ftot
    
# combine
def count_fits(products, boxes):
    fit = 0
    product_i = 0
    boxes_i = 0
    while boxes_i < len(boxes):
        while product_i < len(products) and width(products[product_i]) <= width(boxes[boxes_i]):
            product_i += 1
        fit += product_i
        boxes_i += 1
    return fit


def combine(pl, pr, bl, br):
    br_to_pl_fit = count_fits(pl, br)

    if len(pr) > 0:
        d = min(list(map(length, pr)))
        d_boxes = [box for box in bl if length(box) == d]
        d_products = [product for product in pr if length(product) == d]
        br_to_pl_fit += count_fits(d_products, d_boxes)

    return br_to_pl_fit

# brute force
def brute_fits(p, b):
    total_fit = 0
    for box in b:
        for product in p:
            if product[1] <= box[1] and product[2] <= box[2]:
                total_fit += 1
    return total_fit

# output total fit
print(totalfit(products, boxes))