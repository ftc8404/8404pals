package com.storefront.utilities;

import com.storefront.model.*;
import org.springframework.stereotype.Component;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

@Component
public class SampleData {

    public SampleData() {

    }

    public static List<Users> createSampleUsersHistory() {


        // Random Users #1
        List<UsersAction> usersActions = getRandomUsersActions();
        List<Users> usersList = new ArrayList<>();
        List<UsersStatusEvent> usersStatusEventList = new ArrayList<>();
        usersStatusEventList.add(new UsersStatusEvent(UsersStatusType.CREATED));
        usersStatusEventList.add(new UsersStatusEvent(UsersStatusType.REJECTED, "Unable to get data. Not correct permissions"));
        usersList.add(new Users(usersStatusEventList, usersActions));

        // Random Users #2
        usersActions = getRandomUsersActions();
        usersStatusEventList = new ArrayList<>();
        usersStatusEventList.add(new UsersStatusEvent(UsersStatusType.CREATED));
        usersStatusEventList.add(new UsersStatusEvent(UsersStatusType.APPROVED));
        usersStatusEventList.add(new UsersStatusEvent(UsersStatusType.PROCESSING));
        usersList.add(new Users(usersStatusEventList, usersActions));

        // Random Users #3
        usersActions = getRandomUsersActions();
        usersStatusEventList = new ArrayList<>();
        usersStatusEventList.add(new UsersStatusEvent(UsersStatusType.CREATED));
        usersStatusEventList.add(new UsersStatusEvent(UsersStatusType.APPROVED));
        usersStatusEventList.add(new UsersStatusEvent(UsersStatusType.PROCESSING));
        usersStatusEventList.add(new UsersStatusEvent(UsersStatusType.ON_HOLD, "Still waiting for data"));
        usersStatusEventList.add(new UsersStatusEvent(UsersStatusType.CANCELLED, "Fetch for data has been cancelled"));
        usersList.add(new Users(usersStatusEventList, usersActions));

        // Random Users #4
        usersActions = getRandomUsersActions();
        usersStatusEventList = new ArrayList<>();
        usersStatusEventList.add(new UsersStatusEvent(UsersStatusType.CREATED));
        usersStatusEventList.add(new UsersStatusEvent(UsersStatusType.APPROVED));
        usersStatusEventList.add(new UsersStatusEvent(UsersStatusType.PROCESSING));
        usersStatusEventList.add(new UsersStatusEvent(UsersStatusType.RECEIVED));
        usersList.add(new Users(usersStatusEventList, usersActions));

        // Random Users #5 Pending fulfillment...
        usersActions = getRandomUsersActions();
        usersStatusEventList = new ArrayList<>();
        usersStatusEventList.add(new UsersStatusEvent(UsersStatusType.CREATED));
        usersStatusEventList.add(new UsersStatusEvent(UsersStatusType.APPROVED));
        usersList.add(new Users(usersStatusEventList, usersActions));

        return usersList;
    }

    private static List<UsersAction> getRandomUsersActions() {

        List<Actions> actionList = createSampleActionss();
        List<UsersAction> usersActions = new ArrayList<>();
        for (int i = 0; i < getRandomActionsQuantity(); i++) {
            usersActions.add(new UsersAction(actionList.get(getRandomActionsListIndex()), getRandomActionsQuantity()));
        }
        return usersActions;
    }
}