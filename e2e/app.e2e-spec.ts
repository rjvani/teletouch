import { TeletouchApiPage } from './app.po';

describe('teletouch-api App', function() {
  let page: TeletouchApiPage;

  beforeEach(() => {
    page = new TeletouchApiPage();
  });

  it('should display message saying app works', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('app works!');
  });
});
