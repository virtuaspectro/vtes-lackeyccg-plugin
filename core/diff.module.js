module.exports = {
  VALUE_CREATED: 'created',
  VALUE_UPDATED: 'updated',
  VALUE_DELETED: 'deleted',
  VALUE_UNCHANGED: 'unchanged',
  map: function (obj1, obj2) {
    if (this.isFunction(obj1) || this.isFunction(obj2)) {
      throw new Error('Invalid argument. Function given, object expected.');
    }
    if (this.isValue(obj1) || this.isValue(obj2)) {
      return {
        type: this.compareValues(obj1, obj2),
        data: obj1 === undefined ? obj2 : obj1,
      };
    }

    var diff = {};
    for (var key in obj1) {
      if (this.isFunction(obj1[key])) {
        continue;
      }

      var value2 = undefined;
      if (obj2[key] !== undefined) {
        value2 = obj2[key];
      }

      diff[key] = this.map(obj1[key], value2);
    }
    for (var obj2key in obj2) {
      if (this.isFunction(obj2[obj2key]) || diff[obj2key] !== undefined) {
        continue;
      }

      diff[obj2key] = this.map(undefined, obj2[obj2key]);
    }

    return diff;
  },
  compareValues: function (value1, value2) {
    if (value1 === value2) {
      return this.VALUE_UNCHANGED;
    }
    if (
      this.isDate(value1) &&
      this.isDate(value2) &&
      value1.getTime() === value2.getTime()
    ) {
      return this.VALUE_UNCHANGED;
    }
    if (value1 === undefined) {
      return this.VALUE_CREATED;
    }
    if (value2 === undefined) {
      return this.VALUE_DELETED;
    }
    return this.VALUE_UPDATED;
  },
  isFunction: function (x) {
    return Object.prototype.toString.call(x) === '[object Function]';
  },
  isArray: function (x) {
    return Object.prototype.toString.call(x) === '[object Array]';
  },
  isDate: function (x) {
    return Object.prototype.toString.call(x) === '[object Date]';
  },
  isObject: function (x) {
    return Object.prototype.toString.call(x) === '[object Object]';
  },
  isValue: function (x) {
    return !this.isObject(x) && !this.isArray(x);
  },
  compare: function (oldCards, newCards) {
    const matches = [];
    const changes = [];
    const addedCards = [];

    newCards.every((newCard) => {
      const card = oldCards.find((oldCard) => oldCard.Id === newCard.Id);
      if (card) {
        matches.push(this.map(newCard, card));
        return true;
      }
      addedCards.push(newCard);
      return true;
    });

    matches.forEach((card) => {
      Object.keys(card).every((param) => {
        if (card[param].type !== 'updated') return true;
        changes.push(card);
        return false;
      });
    });

    const totalChanges = changes.length + addedCards.length;

    return { changes, addedCards, totalChanges };
  },
  get: function (cardLists) {
    const changed = {};
    let affectedCards = [];
    let totalChanges = 0;

    ['crypt', 'library'].forEach((type) => {
      changed[type] = this.compare(cardLists[type].old, cardLists[type].new);
      const changedCardNames = changed[type].changes.map(
        (card) => card.Name.data,
      );
      const newCardNames = changed[type].addedCards.map(
        (card) => card.Name.data,
      );

      affectedCards = affectedCards
        .concat(changedCardNames)
        .concat(newCardNames);
      totalChanges += changed[type].totalChanges;
    });

    return { changed, affectedCards, totalChanges };
  },
};
