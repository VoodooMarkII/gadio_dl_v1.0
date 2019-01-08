import GadioListFetcher
import Database
import argparse
import DetailFetcher
import utils


def init_prog():
    print('Initializing database')
    if not utils.is_up_to_date():
        db = Database.Database()
        print('Fetching info from Gcores.')
        glf = GadioListFetcher.GadioListFtecher()
        gadio_list = glf.generate_gadio_list()
        db.write_gadio_list(*gadio_list)
    print('Initialization complete.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mode', help='Select download mode.', choices=['single', 'all'])
    parser.add_argument('-t', '--title', help='The title of Gadio.')
    parser.add_argument('-tl', '--timeline', help='Download timeline?', action='store_true')
    args = parser.parse_args()

    init_prog()
    db_main = Database.Database()
    gadio_list = []
    if args.mode == 'all':
        gadio_list = db_main.select_gadio('gadio')
    elif args.mode == 'single':
        if args.title:
            gadio_list = db_main.select_gadio('gadio', "title='%s'" % args.title)

    if len(gadio_list):
        print('%d gadio is/are found, start downloading.' % len(gadio_list))
        for g in gadio_list:
            df = DetailFetcher.DetailFetcher(g)
            df.download(dl_timeline_flag=args.timeline)
    else:
        print('0 gadio is found, download abort.')
