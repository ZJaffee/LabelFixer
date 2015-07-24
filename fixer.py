# -*- coding: UTF-8 -*-
import time
import os
import sys
import eyeD3

TEST_ONLY = False

def main():
    start_time = time.time()
    fix_count = 0
    skip_count = 0
    filename_encoding = sys.getfilesystemencoding()

    for (dirpath, dirnames, filenames) in os.walk(u"D:\\Local Audio"):
        try:
            print dirpath
        except UnicodeEncodeError, e:
            pass
        for name in filenames:
            fullpath = os.path.join(dirpath, name)

            # magicpath allows us to get around maximum path length limitations
            # unicodepath = fullpath.decode(filename_encoding)
            # magicpath = unicode("\\\\?\\") + unicodepath
            magicpath = unicode("\\\\?\\") + fullpath

            if magicpath.endswith(".mp3"):
                try:
                    print name
                except UnicodeEncodeError:
                    print "Non-Ascii Filename Processed"
                tag = eyeD3.Tag()
                tag.link(magicpath)
                if not TEST_ONLY and not is_fixed(tag):
                    fix_count += 1
                    fix_mp3(tag)
                else:
                    skip_count += 1

    end_time = time.time()
    print "FINISHED IN %s" % timediff(start_time, end_time)
    print "MODIFIED %s MP3's" % fix_count
    print "SKIPPED %s MP3's" % skip_count
    raw_input("HIT ENTER TO QUIT...")
    


def timediff(start_time, end_time):
    runtime = end_time - start_time # in seconds

    days = hours = minutes = seconds = 0
    MINUTE = 60
    HOUR = MINUTE * 60
    DAY = HOUR * 24
    if runtime >= DAY:
        days = int(runtime / DAY)
        runtime -= days * DAY
    if runtime >= HOUR:
        hours = int(runtime / HOUR)
        runtime -= hours * HOUR
    if runtime >= MINUTE:
        minutes = int(runtime / MINUTE)
        runtime -= minutes * MINUTE
    seconds = runtime

    return "%s days, %s hours, %s minutes, % seconds" % (
        days, hours, minutes, seconds
    )


def fix_mp3(tag):
    label = tag.getPublisher()
    if label:
        tag.removeComments()
        tag.addComment("Label: " + label)
        tag.update()


def is_fixed(tag):
    comment_frames = tag.getComments()
    # If there's no comments, it's definitely not fixed
    if not comment_frames:
        return False
    
    # If there are multiple comments, we have to "fix" that
    # in order for VirtualDJ to display the correct comment
    if len(comment_frames) != 1:
        return False

    # If there's just one comment, see if it's correct, if
    # so we can skip it and save time.
    comment = comment_frames[0].comment
    label = tag.getPublisher()
    if not label:
        return True
    elif not comment or not comment == "Label: " + label:
        return False
    else:
        return True


if __name__ == "__main__":
    main()
