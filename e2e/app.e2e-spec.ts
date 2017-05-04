import { TopPage } from './app.po';

describe('top App', function() {
  let page: TopPage;

  beforeEach(() => {
    page = new TopPage();
  });

  it('should display message saying app works', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('app works!');
  });
});
